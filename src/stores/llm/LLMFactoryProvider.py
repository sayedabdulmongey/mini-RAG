from .LLMEnums import LLMEnums

from providers import CoHereProvider, OpenAIProvider


class LLMFactoryProvider:

    def __init__(self, config: dict):
        self.config = config

    def create_provider(self, provider: str):

        if provider == LLMEnum.OPENAI.value:
            return OpenAIProvider(
                self.config.OPENAI_API_KEY,
                self.config.OPENAI_URL_BASE,
                self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                self.config.DEFAULT_MAX_NEW_TOKENS,
                self.config.DEFAULT_TEMPERATURE,
            )

        elif provider == LLMEnum.COHERE.value:
            return CoHereProvider(
                self.config.COHERE_API_KEY,
                self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                self.config.DEFAULT_MAX_NEW_TOKENS,
                self.config.DEFAULT_TEMPERATURE,
            )

        return None
