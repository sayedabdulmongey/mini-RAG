from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME : str
    APP_VERSION : str
    OPENAI_API_KEY : str 
    
    FILE_ALLOWED_TYPES : list = ['text/plain','application/pdf']
    FILE_ALLOWED_SIZE : int
    FILE_DEFAULT_CHUNK : int

    MONGO_URL : str
    MONGO_DATABASE:str

    class Config:
        env_file = '.env'

def get_settings():
    return Settings()