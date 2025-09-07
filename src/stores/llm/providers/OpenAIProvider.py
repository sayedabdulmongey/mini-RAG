from openai import OpenAI
from ..LLMInterface import LLMInterface
from ..LLMEnums import LLMEnums, OpenAIEnums
from logging import getLogger

from typing import Union, List


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
            base_url=self.base_url if self.base_url and len(
                self.base_url) else None
        )

        self.enums = OpenAIEnums

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
                role=OpenAIEnums.USER.value
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

    def get_embedding(self, text: Union[str, List[str]], document_type: str = None):
        if not self.client:
            self.logger.error("OpenAI client not initialized")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model ID not set")
            return None

        response = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=self.process_text(text)
        )
        if not response or not response.data or len(response.data) == 0:
            self.logger.error("Error in OpenAI Embedding response")
            return None

        # Return all embeddings as a list
        return [item.embedding for item in response.data]

    def construct_prompt(self, prompt: str, role: str):
        return {
            'role': role,
            'content': prompt
        }

    def process_text(self, text: Union[str, list[str]]) -> list:
        if isinstance(text, str):
            return [text[:self.default_max_input_characters].strip()]
        elif isinstance(text, list):
            return [t[:self.default_max_input_characters].strip() for t in text]
        else:
            self.logger.error(
                "Input to process_text must be a string or list of strings")
            return []
