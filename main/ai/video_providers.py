"""Concrete async-video adapters. Endpoints default to each platform's documented
API but remain overridable via provider.extra_config (submit_path/poll_path)."""
from .video_base import VideoRESTAdapter


class SeedanceAdapter(VideoRESTAdapter):
    """ByteDance Seedance via BytePlus ModelArk."""
    default_base = 'https://ark.ap-southeast.bytepluses.com'
    default_submit_path = '/api/v3/contents/generations/tasks'
    default_poll_path = '/api/v3/contents/generations/tasks/{job_id}'

    def build_submit_payload(self, prompt, inputs):
        payload = {
            'model': self.model,
            'content': [{'type': 'text', 'text': prompt}],
        }
        payload.update(self.config.get('payload_defaults', {}))
        return payload


class WanAdapter(VideoRESTAdapter):
    """Alibaba WAN via DashScope async API."""
    default_base = 'https://dashscope-intl.aliyuncs.com'
    default_submit_path = '/api/v1/services/aigc/video-generation/video-synthesis'
    default_poll_path = '/api/v1/tasks/{job_id}'

    def _headers(self):
        headers = super()._headers()
        headers['X-DashScope-Async'] = 'enable'
        return headers

    def build_submit_payload(self, prompt, inputs):
        payload = {
            'model': self.model,
            'input': {'prompt': prompt},
            'parameters': self.config.get('payload_defaults', {}),
        }
        return payload

    def parse_submit_response(self, data):
        task_id = (data.get('output') or {}).get('task_id')
        if not task_id:
            from .base import AIProviderError
            raise AIProviderError(f'DashScope returned no task_id: {str(data)[:200]}')
        return task_id

    def parse_poll_response(self, data):
        from .base import VideoJobStatus
        output = data.get('output') or {}
        status = str(output.get('task_status', '')).upper()
        if status == 'SUCCEEDED':
            return VideoJobStatus(status='succeeded', video_url=output.get('video_url'))
        if status in ('FAILED', 'CANCELED'):
            return VideoJobStatus(status='failed', error=str(output.get('message') or output)[:500])
        return VideoJobStatus(status='running')


class HiggsfieldAdapter(VideoRESTAdapter):
    """Higgsfield platform API - endpoints via extra_config as the API evolves."""
    default_base = 'https://platform.higgsfield.ai'
    default_submit_path = '/v1/text2video'
    default_poll_path = '/v1/jobs/{job_id}'
