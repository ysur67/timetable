from typing import Literal

from litestar.types import Method
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class CorsSettings(BaseModel):
    allow_origins: list[str]
    allow_methods: list[Literal["*"] | Method]
    allow_headers: list[str]
    allow_credentials: bool


class LitestarAppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="api_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    cors: CorsSettings
