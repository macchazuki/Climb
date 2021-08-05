from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env.dev"


class TestSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env.test"


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_test_settings():
    return TestSettings()
