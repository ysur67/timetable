from collections.abc import Awaitable, Callable
from typing import Annotated, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aioinject import Inject, inject

from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand
from core.domain.user.dtos import GetOrCreateUserDto


class ChatCurrentUserMiddleware(BaseMiddleware):
    @inject
    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
        command: Annotated[GetOrCreateUserCommand, Inject],
    ) -> Any:  # noqa: ANN401
        user = await command.execute(GetOrCreateUserDto(telegram_id=str(event.chat.id)))
        data["user"] = user
        return await handler(event, data)


class CallbackCurrentUserMiddleware(BaseMiddleware):
    @inject
    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: dict[str, Any],
        command: Annotated[GetOrCreateUserCommand, Inject],
    ) -> Any:  # noqa: ANN401
        if event.message is None:
            raise NotImplementedError
        user = await command.execute(
            GetOrCreateUserDto(telegram_id=str(event.message.chat.id)),
        )
        data["user"] = user
        return await handler(event, data)
