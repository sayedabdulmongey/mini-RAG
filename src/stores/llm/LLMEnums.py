from enum import Enum


class LLMEnums(Enum):

    OPENAI = 'OPENAI'
    GEMINI = 'GEMINI'
    COHERE = 'COHERE'


class OpenAIEnums(Enum):

    USER = 'user'
    SYSTEM = 'developer'
    ASSISTANT = 'assistant'


class CoHereEnums(Enum):

    USER = 'user'
    SYSTEM = 'system'
    ASSISTANT = 'assistant'

    DOCUMENT = 'search_document'
    QUERY = 'search_query'


class DocumentTypeEnums(Enum):

    DOCUMENT = 'document'
    QUERY = 'query'
