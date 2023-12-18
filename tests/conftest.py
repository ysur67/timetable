import os
from collections.abc import AsyncIterator

import dotenv
import pytest
from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncSession

dotenv.load_dotenv(".env")


pytest_plugins = [
    "anyio",
    "tests.plugins.shared_objects",
    "tests.plugins.repositories",
    "tests.plugins.services",
    "tests.plugins.commands",
]


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def db_driver() -> AsyncIterator[AsyncDriver]:
    url = os.environ["TEST_DATABASE_URL"]
    username = os.environ["TEST_DATABASE_USERNAME"]
    password = os.environ["TEST_DATABASE_PASSWORD"]
    async with AsyncGraphDatabase.driver(
        url,
        auth=(username, password),
    ) as driver:
        yield driver


@pytest.fixture()
async def session(db_driver: AsyncDriver) -> AsyncIterator[AsyncSession]:
    database = os.environ["TEST_DATABASE_NAME"]
    async with db_driver.session(database=database) as session:
        yield session
        await session.run("MATCH (n) DETACH DELETE n;")
