from collections.abc import AsyncIterator
from contextlib import aclosing, asynccontextmanager

from litestar import Litestar
from litestar.config.cors import CORSConfig

from di import create_container
from lib.settings.litestar import LitestarAppSettings


@asynccontextmanager
async def _lifespan(_app: Litestar) -> AsyncIterator[None]:
    container = create_container()
    async with aclosing(container):
        yield


def create_app() -> Litestar:
    app_settings = LitestarAppSettings()
    cors_config = CORSConfig(
        allow_origins=app_settings.cors.allow_origins,
        allow_methods=app_settings.cors.allow_methods,
        allow_headers=app_settings.cors.allow_headers,
        allow_credentials=app_settings.cors.allow_credentials,
    )
    return Litestar(
        lifespan=[_lifespan],
        cors_config=cors_config,
    )


app = create_app()
