import functools
from typing import TypeVar

from pydantic_settings import BaseSettings, SettingsConfigDict

TSettings = TypeVar("TSettings", bound=BaseSettings)


def get_settings(cls: type[TSettings]) -> TSettings:
    return cls()


get_settings = functools.lru_cache(get_settings)  # Mypy moment


class NeoSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database_")

    driver: str = "neo4j"

    host: str
    port: int
    username: str
    password: str
    name: str

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.host}:{self.port}"
