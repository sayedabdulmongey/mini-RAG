from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''
    Settings Class for the FastAPI Application
    In this class, we define the settings for the FastAPI Application that are loaded from the .env file
    '''
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list = ['text/plain',
                                'application/pdf']  # allowed types (txt, pdf)
    FILE_ALLOWED_SIZE: int
    FILE_DEFAULT_CHUNK: int

    MONGO_URL: str
    MONGO_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    COHERE_API_KEY: str

    OPENAI_API_KEY: str
    OPENAI_URL_BASE: str

    GOOGLE_API_KEY: str

    GENERATION_MODEL_ID: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_SIZE: int

    DEFAULT_INPUT_MAX_CHARACTERS: int
    DEFAULT_MAX_NEW_TOKENS: int
    DEFAULT_TEMPERATURE: int

    class Config:
        env_file = '.env'


def get_settings():
    return Settings()
