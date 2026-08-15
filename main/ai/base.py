"""Adapter interface for AI providers."""
from dataclasses import dataclass


class AIProviderError(Exception):
    """User-displayable provider failure; message is stored on AIGeneration.error."""


@dataclass
class TextResult:
    text: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    model: str = ''


@dataclass
class ImageResult:
    content: bytes
    mime_type: str = 'image/png'
    model: str = ''


@dataclass
class VideoJobStatus:
    status: str  # running | succeeded | failed
    video_url: str | None = None
    video_bytes: bytes | None = None
    error: str = ''


class AIAdapter:
    """Base adapter. Subclasses implement the operations their provider supports."""

    def __init__(self, provider, model=None):
        self.provider = provider
        self.model = model or provider.default_model
        self.config = provider.extra_config or {}

    # images: list of (bytes, mime_type) tuples for vision input
    def generate_text(self, system_prompt, user_prompt, images=None) -> TextResult:
        raise AIProviderError('This provider does not support text generation.')

    def generate_image(self, prompt, input_images=None) -> ImageResult:
        raise AIProviderError('This provider does not support image generation.')

    def submit_video(self, prompt, inputs) -> str:
        raise AIProviderError('This provider does not support video generation.')

    def poll_video(self, job_id) -> VideoJobStatus:
        raise AIProviderError('This provider does not support video generation.')

    def test_connection(self) -> str:
        raise AIProviderError('Test not implemented for this provider.')

    # helpers
    @property
    def timeout(self):
        return self.config.get('timeout', 120)

    @property
    def max_tokens(self):
        return int(self.config.get('max_tokens', 8000))
