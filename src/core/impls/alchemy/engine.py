from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from lib.settings import get_settings
from lib.settings.database import PostgresSettings

_settings = get_settings(PostgresSettings)

engine = create_async_engine(
    _settings.url,
    future=True,
    pool_size=20,
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo=_settings.echo,
)

async_session_factory = async_sessionmaker(bind=engine)
