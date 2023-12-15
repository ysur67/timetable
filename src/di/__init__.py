import functools
from collections.abc import Iterable

import aioinject
from pydantic_settings import BaseSettings

from core.impls.neo.dependencies import get_driver, get_session
from lib.settings import NeoSettings, get_settings

SETTINGS = (NeoSettings,)


def _register_settings(
    container: aioinject.Container,
    *,
    settings_classes: Iterable[type[BaseSettings]],
) -> None:
    for settings_cls in settings_classes:
        factory = functools.partial(get_settings, settings_cls)
        container.register(aioinject.Singleton(factory, type_=settings_cls))


@functools.lru_cache
def create_container() -> aioinject.Container:
    container = aioinject.Container()
    container.register(aioinject.Singleton(get_driver))
    container.register(aioinject.Callable(get_session))

    _register_settings(container, settings_classes=SETTINGS)

    return container
