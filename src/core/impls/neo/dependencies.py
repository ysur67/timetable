import contextlib
from collections.abc import AsyncIterator

from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncSession

from lib.settings import NeoSettings


@contextlib.asynccontextmanager
async def get_driver(settings: NeoSettings) -> AsyncIterator[AsyncDriver]:
    async with AsyncGraphDatabase.driver(
        settings.url,
        auth=(settings.username, settings.password),
    ) as driver:
        yield driver


@contextlib.asynccontextmanager
async def get_session(
    driver: AsyncDriver,
    settings: NeoSettings,
) -> AsyncIterator[AsyncSession]:
    async with driver.session(database=settings.name) as session:
        yield session
