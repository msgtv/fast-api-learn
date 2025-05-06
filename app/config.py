from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DB_URL: Optional[str] = None

    @model_validator(mode='after')
    def get_database_url(self):
        self.DB_URL = (
            f'postgresql+asyncpg://'
            f'{self.DB_USER}:{self.DB_PASS}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )
        return self

    class Config:
        env_file = ".env"


settings = Settings()

print(settings.DB_URL)
