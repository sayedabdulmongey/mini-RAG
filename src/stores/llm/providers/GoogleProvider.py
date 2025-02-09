from google import genai

from ..LLMInterface import LLMInterface
from ..LLMEnums import GoogleEnums, DocumentTypeEnums
from logging import getLogger


class GoogleProvider(LLMInterface):

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

        self.client = genai.Client(
            api_key=self.api_key
        )

        self.enums = GoogleEnums

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
            self.logger.error("Gemini client not initialized")
            return None

        if not self.generation_model_id:
            self.logger.error("Model ID not set")
            return None

        chat_history.append(
            self.construct_prompt(
                prompt=prompt,
                role=GoogleEnums.USER.value
            )
        )

        max_new_tokens = max_new_tokens if max_new_tokens else self.default_max_output_tokens
        temperature = temperature if temperature else self.default_temperature

        print(chat_history)
        print(self.generation_model_id)

        response = self.client.models.generate_content(
            model=self.generation_model_id,
            contents=chat_history,
            config={
                'max_output_tokens': max_new_tokens,
                'temperature': temperature
            }
        )

        if not response or not response.text:
            self.logger.error("Error in Gemini text generation response")
            return None

        return response.text

    def get_embedding(self, text: str, document_type: str = None):

        if not self.client:
            self.logger.error("Google client not initialized")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model ID not set")
            return None

        input_type = GoogleEnums.DOCUMENT.value if document_type == DocumentTypeEnums.DOCUMENT.value else GoogleEnums.QUERY.value

        response = self.client.models.embed_content(
            model=self.embedding_model_id,
            contents=self.process_text(text),
            config={
                'task_type': input_type
            }
        )

        if not response or not response.embeddings or len(response.embeddings) == 0 or not response.embeddings[0].values:
            self.logger.error("Error in Google Embedding response")
            return None

        return response.embeddings[0].values

    def construct_prompt(self, prompt, role):
        return '\n'.join(
            [
                f'role: {role}',
                f'content: {self.process_text(prompt)}'
            ]
        )

    def process_text(self, text):
        return text[:self.default_max_input_characters].strip()
