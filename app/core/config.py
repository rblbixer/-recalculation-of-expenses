from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    bot_token: str = Field("", alias="BOT_TOKEN")
    admin_ids: List[int] = Field(default_factory=list, alias="ADMIN_IDS")

    database_url: str = Field(..., alias="DATABASE_URL")

    api_host: str = Field("0.0.0.0", alias="API_HOST")
    api_port: int = Field(8000, alias="API_PORT")
    debug: bool = Field(True, alias="DEBUG")
    testing: bool = Field(False, alias="TESTING")

    @field_validator("admin_ids", mode="before")
    @classmethod
    def split_admin_ids(cls, value: str | List[int]) -> List[int]:
        if isinstance(value, list):
            return [int(v) for v in value]
        if not value:
            return []
        return [int(v.strip()) for v in value.split(",") if v.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

