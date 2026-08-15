"""AI adapter registry."""
from .base import AIAdapter, AIProviderError, ImageResult, TextResult, VideoJobStatus


def get_adapter(provider, model_override=None) -> AIAdapter:
    """Return an adapter instance for an AIProvider row."""
    # Imports deferred so a missing optional dependency only breaks its own adapter
    from .anthropic_adapter import AnthropicAdapter
    from .gemini import GeminiAdapter
    from .openai_compat import DeepSeekAdapter, OpenAICompatAdapter
    from .video_providers import HiggsfieldAdapter, SeedanceAdapter, WanAdapter

    registry = {
        'anthropic': AnthropicAdapter,
        'openai_compatible': OpenAICompatAdapter,
        'deepseek': DeepSeekAdapter,
        'gemini': GeminiAdapter,
        'seedance': SeedanceAdapter,
        'wan': WanAdapter,
        'higgsfield': HiggsfieldAdapter,
    }
    cls = registry.get(provider.adapter_type)
    if cls is None:
        raise AIProviderError(f'Unknown adapter type: {provider.adapter_type}')
    return cls(provider, model_override or None)
