from pydantic_settings import BaseSettings, SettingsConfigDict


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
