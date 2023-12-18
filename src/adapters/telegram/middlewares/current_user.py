from collections.abc import Awaitable, Callable
from typing import Annotated, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from aioinject import Inject, inject

from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand
from core.domain.user.dtos import GetOrCreateUserDto


class CurrentUserMiddleware(BaseMiddleware):
    @inject
    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
        command: Annotated[GetOrCreateUserCommand, Inject],
    ) -> Any:  # noqa: ANN401
        user = await command.execute(GetOrCreateUserDto(telegram_id=event.chat.id))
        data["user"] = user
        return await handler(event, data)
