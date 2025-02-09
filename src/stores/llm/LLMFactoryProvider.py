from .LLMEnums import LLMEnums

from .providers import CoHereProvider, OpenAIProvider, GoogleProvider


class LLMFactoryProvider:

    def __init__(self, config: dict):
        self.config = config

    def create_provider(self, provider: str):

        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                base_url=self.config.OPENAI_URL_BASE,
                default_max_input_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                default_max_output_tokens=self.config.DEFAULT_MAX_NEW_TOKENS,
                default_temperature=self.config.DEFAULT_TEMPERATURE,
            )

        elif provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_max_input_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                default_max_output_tokens=self.config.DEFAULT_MAX_NEW_TOKENS,
                default_temperature=self.config.DEFAULT_TEMPERATURE,
            )
        elif provider == LLMEnums.GOOGLE.value:
            return GoogleProvider(
                api_key=self.config.GOOGLE_API_KEY,
                default_max_input_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                default_max_output_tokens=self.config.DEFAULT_MAX_NEW_TOKENS,
                default_temperature=self.config.DEFAULT_TEMPERATURE,
            )
        return None
