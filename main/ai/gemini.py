"""Google Gemini adapter via the REST generativelanguage API.
Handles text (gemini-2.5-flash etc.) and image generation/editing via
gemini-2.5-flash-image ("Nano Banana") which returns base64 inline image parts."""
import base64

import requests

from .base import AIAdapter, AIProviderError, ImageResult, TextResult

DEFAULT_BASE = 'https://generativelanguage.googleapis.com'


class GeminiAdapter(AIAdapter):
    @property
    def base(self):
        return (self.provider.base_url or DEFAULT_BASE).rstrip('/')

    def _post(self, model, payload):
        if not self.provider.api_key:
            raise AIProviderError('No API key configured for this provider.')
        url = f'{self.base}/v1beta/models/{model}:generateContent'
        try:
            resp = requests.post(url, json=payload, timeout=(10, self.timeout),
                                 headers={'x-goog-api-key': self.provider.api_key,
                                          'Content-Type': 'application/json'})
        except requests.RequestException as exc:
            raise AIProviderError(f'Could not reach Gemini: {exc.__class__.__name__}')
        if resp.status_code in (401, 403):
            raise AIProviderError('Invalid Gemini API key.')
        if resp.status_code == 429:
            raise AIProviderError('Gemini rate limit reached. Try again shortly.')
        if not resp.ok:
            raise AIProviderError(f'Gemini error {resp.status_code}: {resp.text[:200]}')
        return resp.json()

    def _parts(self, prompt, images):
        parts = []
        if images:
            for data, mime in images:
                parts.append({'inline_data': {
                    'mime_type': mime,
                    'data': base64.standard_b64encode(data).decode(),
                }})
        parts.append({'text': prompt})
        return parts

    def generate_text(self, system_prompt, user_prompt, images=None) -> TextResult:
        payload = {
            'system_instruction': {'parts': [{'text': system_prompt}]},
            'contents': [{'role': 'user', 'parts': self._parts(user_prompt, images)}],
            'generationConfig': {'maxOutputTokens': self.max_tokens},
        }
        data = self._post(self.model, payload)
        try:
            parts = data['candidates'][0]['content']['parts']
            text = ''.join(p.get('text', '') for p in parts)
        except (KeyError, IndexError):
            raise AIProviderError('Gemini returned no content (possibly blocked).')
        if not text:
            raise AIProviderError('Gemini returned an empty response.')
        usage = data.get('usageMetadata', {})
        return TextResult(text=text, tokens_in=usage.get('promptTokenCount'),
                          tokens_out=usage.get('candidatesTokenCount'), model=self.model)

    def generate_image(self, prompt, input_images=None) -> ImageResult:
        image_model = self.config.get('image_model', self.model)
        payload = {'contents': [{'role': 'user', 'parts': self._parts(prompt, input_images)}]}
        data = self._post(image_model, payload)
        try:
            parts = data['candidates'][0]['content']['parts']
        except (KeyError, IndexError):
            raise AIProviderError('Gemini returned no content (possibly blocked).')
        for part in parts:
            inline = part.get('inlineData') or part.get('inline_data')
            if inline and inline.get('data'):
                mime = inline.get('mimeType') or inline.get('mime_type') or 'image/png'
                return ImageResult(content=base64.b64decode(inline['data']),
                                   mime_type=mime, model=image_model)
        raise AIProviderError('Gemini returned no image. Check that the model supports image output.')

    def test_connection(self) -> str:
        result = self.generate_text('Reply with exactly: OK', 'Say OK')
        return f'OK (model {result.model})'
