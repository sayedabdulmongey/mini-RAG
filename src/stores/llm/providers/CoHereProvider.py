
from typing import Union
from cohere import ClientV2
from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnums
from logging import getLogger


class CoHereProvider(LLMInterface):

    def __init__(self, api_key: str,
                 default_max_input_characters: int = 1000,
                 default_max_output_tokens: int = 1000,
                 default_temperature: float = 0.1):

        self.api_key = api_key

        self.default_max_input_characters = default_max_input_characters
        self.default_max_output_tokens = default_max_output_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = ClientV2(
            api_key=self.api_key
        )

        self.enums = CoHereEnums

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
            self.logger.error("Cohere client not initialized")
            return None

        if not self.generation_model_id:
            self.logger.error("Model ID not set")
            return None

        chat_history.append(
            self.construct_prompt(
                prompt=prompt,
                role=CoHereEnums.USER.value
            )
        )

        max_new_tokens = max_new_tokens if max_new_tokens else self.default_max_output_tokens
        temperature = temperature if temperature else self.default_temperature

        response = self.client.chat(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_new_tokens,
            temperature=temperature
        )

        if not response or not response.message or not response.message.content or len(response.message.content) == 0 or not response.message.content[0].text:
            self.logger.error("Error in Cohere text generation response")
            return None

        return response.message.content[0].text

    def get_embedding(self, text: Union[str, list[str]], document_type: str = None):
        if not self.client:
            self.logger.error("Cohere client not initialized")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model ID not set")
            return None

        input_type = CoHereEnums.DOCUMENT.value if document_type == DocumentTypeEnums.DOCUMENT.value else CoHereEnums.QUERY.value

        response = self.client.embed(
            model=self.embedding_model_id,
            texts=self.process_text(text),
            input_type=input_type,
            embedding_types=["float"]
        )
        if not response or not response.embeddings or not response.embeddings.float or len(response.embeddings.float) == 0:
            self.logger.error("Error in Cohere Embedding response")
            return None

        # Return all embeddings as a list
        return response.embeddings.float

    def construct_prompt(self, prompt, role):
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
