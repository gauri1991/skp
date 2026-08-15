"""Shared machinery for async video providers (submit -> poll -> download).
Endpoints and auth style are configurable per provider row via extra_config,
since these platforms' APIs evolve quickly:

extra_config keys (all optional, adapter ships defaults):
  submit_path, poll_path ("{job_id}" placeholder), auth_style (bearer|header),
  auth_header (when auth_style=header), payload_defaults (dict merged into submit)
"""
import requests

from .base import AIAdapter, AIProviderError, VideoJobStatus


class VideoRESTAdapter(AIAdapter):
    default_base = ''
    default_submit_path = ''
    default_poll_path = ''

    @property
    def base(self):
        base = (self.provider.base_url or self.default_base).rstrip('/')
        if not base:
            raise AIProviderError('No base URL configured for this video provider.')
        return base

    def _headers(self):
        if not self.provider.api_key:
            raise AIProviderError('No API key configured for this provider.')
        style = self.config.get('auth_style', 'bearer')
        if style == 'header':
            return {self.config.get('auth_header', 'X-API-Key'): self.provider.api_key,
                    'Content-Type': 'application/json'}
        return {'Authorization': f'Bearer {self.provider.api_key}',
                'Content-Type': 'application/json'}

    def _request(self, method, path, **kwargs):
        try:
            resp = requests.request(method, f'{self.base}{path}', headers=self._headers(),
                                    timeout=(10, self.timeout), **kwargs)
        except requests.RequestException as exc:
            raise AIProviderError(f'Could not reach video provider: {exc.__class__.__name__}')
        if resp.status_code in (401, 403):
            raise AIProviderError('Invalid API key for this video provider.')
        if not resp.ok:
            raise AIProviderError(f'Video provider error {resp.status_code}: {resp.text[:200]}')
        return resp.json()

    # Subclasses map provider-specific payloads/response shapes
    def build_submit_payload(self, prompt, inputs):
        payload = {'model': self.model, 'prompt': prompt}
        payload.update(self.config.get('payload_defaults', {}))
        return payload

    def parse_submit_response(self, data) -> str:
        for key in ('id', 'task_id', 'job_id'):
            if key in data:
                return str(data[key])
            if isinstance(data.get('output'), dict) and key in data['output']:
                return str(data['output'][key])
        raise AIProviderError(f'Could not find job id in provider response: {str(data)[:200]}')

    def parse_poll_response(self, data) -> VideoJobStatus:
        status = str(data.get('status', '')).lower()
        if status in ('succeeded', 'success', 'completed', 'done'):
            url = (data.get('video_url') or data.get('output', {}).get('video_url')
                   or (data.get('content') or {}).get('video_url'))
            if not url and isinstance(data.get('output'), list) and data['output']:
                url = data['output'][0]
            return VideoJobStatus(status='succeeded', video_url=url)
        if status in ('failed', 'error', 'cancelled', 'canceled'):
            return VideoJobStatus(status='failed', error=str(data.get('error') or data)[:500])
        return VideoJobStatus(status='running')

    def submit_video(self, prompt, inputs) -> str:
        path = self.config.get('submit_path', self.default_submit_path)
        data = self._request('POST', path, json=self.build_submit_payload(prompt, inputs))
        return self.parse_submit_response(data)

    def poll_video(self, job_id) -> VideoJobStatus:
        path = self.config.get('poll_path', self.default_poll_path).format(job_id=job_id)
        return self.parse_poll_response(self._request('GET', path))

    def download_video(self, url) -> bytes:
        try:
            resp = requests.get(url, timeout=(10, 300))
            resp.raise_for_status()
        except requests.RequestException:
            raise AIProviderError('Could not download the generated video.')
        return resp.content

    def test_connection(self) -> str:
        # Cheap reachability check only - a real submit would cost money.
        self._headers()  # validates key presence
        return f'Configured (base {self.base}, model {self.model}). Run a real generation to fully verify.'
