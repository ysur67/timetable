from pydantic_settings import BaseSettings, SettingsConfigDict


class NeoSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="neo_")

    driver: str = "neo4j"

    host: str
    port: int
    username: str
    password: str
    name: str

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.host}:{self.port}"


class SqliteSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database_")

    driver: str = "sqlite+aiosqlite"

    filename: str
    echo: bool = False

    @property
    def url(self) -> str:
        return f"{self.driver}:///{self.filename}"


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database_")

    driver: str = "postgresql+asyncpg"

    host: str
    port: str
    name: str
    user: str
    password: str
    echo: bool = False

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
