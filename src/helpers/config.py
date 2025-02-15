from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    '''
    Settings Class for the FastAPI Application
    In this class, we define the settings for the FastAPI Application that are loaded from the .env file
    '''
    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: List[str]
    FILE_ALLOWED_SIZE: int
    FILE_DEFAULT_CHUNK: int

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    COHERE_API_KEY: str

    OPENAI_API_KEY: str
    OPENAI_URL_BASE: str = None

    GOOGLE_API_KEY: str

    GENERATION_MODEL_ID: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_SIZE: int

    DEFAULT_INPUT_MAX_CHARACTERS: int = None
    DEFAULT_MAX_NEW_TOKENS: int = None
    DEFAULT_TEMPERATURE: float = None

    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str

    DEFAULT_LANGUAGE: str = 'en'
    PRIMARY_LANGUAGE: str

    class Config:
        env_file = '.env'


def get_settings():
    return Settings()
