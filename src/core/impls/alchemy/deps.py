import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from .engine import async_session_factory, engine


@contextlib.asynccontextmanager
async def get_engine() -> AsyncIterator[AsyncEngine]:
    yield engine
    await engine.dispose()


@contextlib.asynccontextmanager
async def get_alchemy_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session
