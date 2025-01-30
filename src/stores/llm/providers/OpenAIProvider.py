from openai import OpenAI
from ..LLMInterface import LLMInterface
from ..LLMEnum import LLMEnum, OpenAIEnum
from logging import getLogger


class OpenAIProvider(LLMInterface):

    def __init__(self, api_key: str, base_url: str = None,
                 default_max_input_characters: int = 1000,
                 default_max_output_tokens: int = 1000,
                 default_temperature: float = 0.1):

        self.api_key = api_key
        self.base_url = base_url

        self.default_max_input_characters = default_max_input_characters
        self.default_max_output_tokens = default_max_output_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        self.logger = getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, embedding_model_id: str, embedding_size: int):
        self.embedding_model_id = embedding_model_id
        self.embedding_size = embedding_size

    def generate_text(self, prompt: str,
                      chat_history: list = [],
                      max_new_tokens: int = None,
                      temperature: float = None):

        if not self.client:
            self.logger.error("OpenAI client not initialized")
            return None

        if not self.generation_model_id:
            self.logger.error("Model ID not set")
            return None

        chat_history.append(
            self.construct_prompt(
                prompt=prompt,
                role=OpenAIEnum.SYSTEM.value
            )
        )

        max_new_tokens = max_new_tokens if max_new_tokens else self.default_max_output_tokens
        temperature = temperature if temperature else self.default_temperature

        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_new_tokens,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message or not response.choices[0].message.content:
            self.logger.error("Error in OpenAI text generation response")
            return None

        return response.choices[0].message.content

    def get_embedding(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("OpenAI client not initialized")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model ID not set")
            return None

        response = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text
        )
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error in OpenAI Embedding response")
            return None
        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: str):
        return {
            'role': role,
            'content': self.process_text(prompt)
        }

    def process_text(self, text: str):
        return text[:self.default_max_input_characters].strip()
