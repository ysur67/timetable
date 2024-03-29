from collections.abc import Awaitable, Callable
from typing import Any

import aioinject
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aioinject import inject


class AioinjectMiddleware(BaseMiddleware):

    def __init__(self, container: aioinject.Container) -> None:
        super().__init__()
        self._container = container

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:  # noqa: ANN401
        async with self._container.context():
            return await handler(event, data)


class CallbackAioinjectMiddleware(BaseMiddleware):

    def __init__(self, container: aioinject.Container) -> None:
        super().__init__()
        self._container = container

    @inject
    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: dict[str, Any],
    ) -> Any:  # noqa: ANN401
        async with self._container.context():
            return await handler(event, data)
