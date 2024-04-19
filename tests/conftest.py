from collections.abc import AsyncIterator

import dotenv
import httpx
import pytest
from litestar import Litestar

from adapters.litestar.app import create_app

dotenv.load_dotenv(".env")


pytest_plugins = [
    "anyio",
    "tests.plugins.database",
    "tests.plugins.shared_objects",
    "tests.plugins.repositories",
    "tests.plugins.commands",
    "tests.plugins.queries",
]


@pytest.fixture(scope="session", autouse=True)
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def worker_id() -> str:
    return "main"


@pytest.fixture(scope="session")
async def litestar_app() -> AsyncIterator[Litestar]:
    app = create_app()
    async with app.lifespan():
        yield app


@pytest.fixture()
async def http_transport(
    litestar_app: Litestar,
) -> AsyncIterator[httpx.AsyncBaseTransport]:
    async with httpx.ASGITransport(app=litestar_app) as transport:  # type: ignore[arg-type]
        yield transport


@pytest.fixture()
async def api_client(http_transport: httpx.AsyncBaseTransport) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        transport=http_transport,
        base_url="http://test",
    )
