from collections.abc import AsyncIterator
from contextlib import aclosing, asynccontextmanager

from aioinject.ext.litestar import AioInjectPlugin
from litestar import Litestar
from litestar.config.cors import CORSConfig

from adapters.litestar.routers import educational_level
from di import create_container
from lib.settings.litestar import LitestarAppSettings


def create_app() -> Litestar:
    app_settings = LitestarAppSettings()
    container = create_container()

    @asynccontextmanager
    async def _lifespan(_app: Litestar) -> AsyncIterator[None]:
        async with aclosing(container):
            yield

    cors_config = CORSConfig(
        allow_origins=app_settings.cors.allow_origins,
        allow_methods=app_settings.cors.allow_methods,
        allow_headers=app_settings.cors.allow_headers,
        allow_credentials=app_settings.cors.allow_credentials,
    )
    return Litestar(
        lifespan=[_lifespan],
        cors_config=cors_config,
        plugins=[AioInjectPlugin(container=container)],
        route_handlers=[educational_level.router],
    )


app = create_app()
