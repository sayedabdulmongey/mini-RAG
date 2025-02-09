from enum import Enum


class LLMEnums(Enum):

    OPENAI = 'OPENAI'
    GOOGLE = 'GOOGLE'
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


class GoogleEnums(Enum):

    USER = 'user'
    SYSTEM = 'developer'
    ASSISTANT = 'assistant'

    DOCUMENT = 'RETRIEVAL_DOCUMENT'
    QUERY = 'RETRIEVAL_QUERY'
