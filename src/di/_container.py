import functools
import itertools
from collections.abc import Iterable
from typing import Any

import aioinject
from pydantic_settings import BaseSettings

import scraping
from adapters.telegram.dependencies import create_bot
from core.domain import user
from core.impls import neo
from core.impls.neo.dependencies import get_driver, get_session
from lib.settings import NeoSettings, get_settings
from lib.settings.telegram import TelegramSettings

SETTINGS = (NeoSettings, TelegramSettings)

MODULES: Iterable[Iterable[aioinject.Provider[Any]]] = [
    neo.providers,
    scraping.providers,
    user.providers,
]


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
    container.register(aioinject.Singleton(create_bot))

    _register_settings(container, settings_classes=SETTINGS)

    for provider in itertools.chain.from_iterable(MODULES):
        container.register(provider)

    return container
