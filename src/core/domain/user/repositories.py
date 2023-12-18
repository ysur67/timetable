from typing import Protocol

from core.models.user import User, UserTelegramId


class UserRepository(Protocol):
    async def get_by_telegram_id(self, ident: UserTelegramId) -> User | None:
        ...

    async def create(self, user: User) -> User:
        ...

    async def save(self, user: User) -> User:
        ...
