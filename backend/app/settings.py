from functools import lru_cache

from pydantic_settings import BaseSettings


class CoreSettings(BaseSettings):
    APP_NAME: str = "Tourism suggester ✨"
    DEBUG: bool = False

    OPENAI_API_KEY: str

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            # "?sslmode=require&channel_binding=require"
        )


class DatabaseSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str


class Settings(CoreSettings, DatabaseSettings):
    pass


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
