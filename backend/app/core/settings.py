
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    APP_NAME: str = "psy-profile-api"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True

    PROVIDER: str = "OPENAI"
    PROVIDER_BASE_URL: str = "https://api.openai.com/v1"
    PROVIDER_API_KEY: str = ""

settings = Settings()
