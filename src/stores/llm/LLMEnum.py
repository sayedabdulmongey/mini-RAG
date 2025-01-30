from enum import Enum


class LLMEnum(Enum):

    OPENAI = 'OPENAI'
    GEMINI = 'GEMINI'
    COHERE = 'COHERE'


class OpenAIEnum(Enum):

    USER = 'user'
    SYSTEM = 'developer'
    ASSISTANT = 'assistant'


class CoHereEnum(Enum):

    USER = 'user'
    SYSTEM = 'system'
    ASSISTANT = 'assistant'

    DOCUMENT = 'search_document'
    QUERY = 'search_query'


class DocumentTypeEnum(Enum):

    DOCUMENT = 'document'
    QUERY = 'query'
