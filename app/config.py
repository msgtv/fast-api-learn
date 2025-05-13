from typing import Optional, Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @model_validator(mode='after')
    def get_database_url(self):
        self.DB_URL = (
            f'postgresql+asyncpg://'
            f'{self.DB_USER}:{self.DB_PASS}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )
        return self

    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str

    @model_validator(mode='after')
    def get_test_database_url(self):
        self.TEST_DB_URL = (
            f'postgresql+asyncpg://'
            f'{self.TEST_DB_USER}:{self.TEST_DB_PASS}@'
            f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'
        )
        return self

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_USER_PASSWORD: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    DB_URL: Optional[str] = None
    TEST_DB_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

print(settings.DB_URL)
