"""
LLM Client Factory — creates LLM clients and model wrappers.

Design:
- Lazy initialization: clients created only when first accessed
- Factory pattern: easy to add new providers (OpenAI, Anthropic, etc.)
- Lazy validation: API keys checked only when client is created, not at startup

Usage in agent files:
    from imtiaz_mart_ai.infrastructure.llm_client import groq_model
    agent = Agent(name="...", model=groq_model, ...)
"""

from agents import AsyncOpenAI, OpenAIChatCompletionsModel

from imtiaz_mart_ai.config.settings import get_settings, require_llm_key


class LLMClient:
    """
    Factory for LLM clients. Creates and caches clients.
    """
    
    _groq_client: AsyncOpenAI | None = None
    _gemini_client: AsyncOpenAI | None = None
    
    @classmethod
    def get_groq_client(cls) -> AsyncOpenAI:
        """Create Groq client on first call, reuse after."""
        if cls._groq_client is None:
            settings = get_settings()
            key = require_llm_key("groq")
            cls._groq_client = AsyncOpenAI(api_key=key, base_url=settings.GROQ_BASE_URL)
        return cls._groq_client
    
    @classmethod
    def get_gemini_client(cls) -> AsyncOpenAI:
        """Create Gemini client on first call, reuse after."""
        if cls._gemini_client is None:
            settings = get_settings()
            key = require_llm_key("gemini")
            cls._gemini_client = AsyncOpenAI(api_key=key, base_url=settings.GEMINI_BASE_URL)
        return cls._gemini_client


# Pre-built model wrappers — import these directly in agent files
groq_model = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",
    openai_client=LLMClient.get_groq_client(),
)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=LLMClient.get_gemini_client(),
)