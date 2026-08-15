"""Anthropic Claude adapter using the official SDK."""
import base64

import anthropic

from .base import AIAdapter, AIProviderError, TextResult


class AnthropicAdapter(AIAdapter):
    def _client(self):
        if not self.provider.api_key:
            raise AIProviderError('No API key configured for this provider.')
        kwargs = {'api_key': self.provider.api_key, 'timeout': 150.0, 'max_retries': 1}
        if self.provider.base_url:
            kwargs['base_url'] = self.provider.base_url
        return anthropic.Anthropic(**kwargs)

    def _build_content(self, user_prompt, images):
        if not images:
            return user_prompt
        content = []
        for data, mime in images:
            content.append({
                'type': 'image',
                'source': {
                    'type': 'base64',
                    'media_type': mime,
                    'data': base64.standard_b64encode(data).decode('utf-8'),
                },
            })
        content.append({'type': 'text', 'text': user_prompt})
        return content

    def generate_text(self, system_prompt, user_prompt, images=None) -> TextResult:
        client = self._client()
        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{'role': 'user', 'content': self._build_content(user_prompt, images)}],
            )
        except anthropic.AuthenticationError:
            raise AIProviderError('Invalid Anthropic API key.')
        except anthropic.RateLimitError:
            raise AIProviderError('Anthropic rate limit reached. Please try again in a minute.')
        except anthropic.APIConnectionError:
            raise AIProviderError('Could not reach the Anthropic API. Please try again.')
        except anthropic.APIStatusError as exc:
            raise AIProviderError(f'Anthropic API error ({exc.status_code}).')

        if response.stop_reason == 'refusal':
            detail = ''
            if getattr(response, 'stop_details', None) and getattr(response.stop_details, 'explanation', None):
                detail = f' {response.stop_details.explanation}'
            raise AIProviderError('The AI declined this request.' + detail)

        text = next((b.text for b in response.content if b.type == 'text'), '')
        if not text:
            raise AIProviderError('The AI returned an empty response. Please try again.')
        return TextResult(
            text=text,
            tokens_in=response.usage.input_tokens,
            tokens_out=response.usage.output_tokens,
            model=response.model,
        )

    def test_connection(self) -> str:
        result = self.generate_text('Reply with exactly: OK', 'Say OK')
        return f'OK (model {result.model}, {result.tokens_out} output tokens)'
