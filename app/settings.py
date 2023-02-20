import pydantic
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings are loaded from .env"""

    DATABASE_URL: pydantic.SecretStr

    class Config:
        frozen = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()  # pyright: ignore
