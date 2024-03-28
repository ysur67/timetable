import dotenv
import pytest

dotenv.load_dotenv(".env")


pytest_plugins = [
    "anyio",
    "tests.plugins.database",
    "tests.plugins.shared_objects",
    "tests.plugins.repositories",
    "tests.plugins.commands",
    "tests.plugins.queries",
]


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def worker_id() -> str:
    return "main"
