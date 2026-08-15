"""Generic OpenAI-compatible REST adapter (chat completions + image generations).
Covers DeepSeek (subclass), OpenAI image models, FLUX-style endpoints, and any
future provider exposing the de-facto standard API."""
import base64

import requests

from .base import AIAdapter, AIProviderError, ImageResult, TextResult

DEFAULT_BASE = 'https://api.openai.com'


class OpenAICompatAdapter(AIAdapter):
    default_base = DEFAULT_BASE

    @property
    def base(self):
        return (self.provider.base_url or self.default_base).rstrip('/')

    def _headers(self):
        if not self.provider.api_key:
            raise AIProviderError('No API key configured for this provider.')
        return {'Authorization': f'Bearer {self.provider.api_key}',
                'Content-Type': 'application/json'}

    def _post(self, path, payload):
        try:
            resp = requests.post(f'{self.base}{path}', json=payload,
                                 headers=self._headers(), timeout=(10, self.timeout))
        except requests.RequestException as exc:
            raise AIProviderError(f'Could not reach the provider: {exc.__class__.__name__}')
        if resp.status_code == 401:
            raise AIProviderError('Invalid API key for this provider.')
        if resp.status_code == 429:
            raise AIProviderError('Provider rate limit reached. Try again shortly.')
        if not resp.ok:
            raise AIProviderError(f'Provider error {resp.status_code}: {resp.text[:200]}')
        return resp.json()

    def generate_text(self, system_prompt, user_prompt, images=None) -> TextResult:
        messages = [{'role': 'system', 'content': system_prompt}]
        if images:
            content = [{'type': 'text', 'text': user_prompt}]
            for data, mime in images:
                b64 = base64.standard_b64encode(data).decode()
                content.append({'type': 'image_url',
                                'image_url': {'url': f'data:{mime};base64,{b64}'}})
            messages.append({'role': 'user', 'content': content})
        else:
            messages.append({'role': 'user', 'content': user_prompt})

        data = self._post(self.config.get('chat_path', '/v1/chat/completions'), {
            'model': self.model,
            'messages': messages,
            'max_tokens': self.max_tokens,
        })
        try:
            text = data['choices'][0]['message']['content']
        except (KeyError, IndexError):
            raise AIProviderError('Unexpected response shape from provider.')
        usage = data.get('usage', {})
        return TextResult(text=text, tokens_in=usage.get('prompt_tokens'),
                          tokens_out=usage.get('completion_tokens'),
                          model=data.get('model', self.model))

    def generate_image(self, prompt, input_images=None) -> ImageResult:
        data = self._post(self.config.get('images_path', '/v1/images/generations'), {
            'model': self.model,
            'prompt': prompt,
            'n': 1,
            'response_format': 'b64_json',
        })
        try:
            b64 = data['data'][0]['b64_json']
        except (KeyError, IndexError):
            raise AIProviderError('Provider returned no image data.')
        return ImageResult(content=base64.b64decode(b64), mime_type='image/png',
                           model=self.model)

    def test_connection(self) -> str:
        result = self.generate_text('Reply with exactly: OK', 'Say OK')
        return f'OK (model {result.model})'


class DeepSeekAdapter(OpenAICompatAdapter):
    default_base = 'https://api.deepseek.com'
