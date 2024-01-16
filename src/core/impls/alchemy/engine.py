from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from lib.settings import get_settings
from lib.settings.database import SqliteSettings

_settings = get_settings(SqliteSettings)

engine = create_async_engine(_settings.url, echo=_settings.echo)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
