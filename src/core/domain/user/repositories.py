from collections.abc import Sequence
from typing import Protocol

from pydantic import BaseModel

from core.models.group import GroupId
from core.models.user import User, UserTelegramId
from lib.filter_ import Unset


class UserFilter(BaseModel):
    selected_group_id: GroupId | None | Unset = Unset.value


class UserRepository(Protocol):
    async def get_by_telegram_id(self, ident: UserTelegramId) -> User | None: ...

    async def create(self, user: User) -> User: ...

    async def save(self, user: User) -> User: ...

    async def get_users(self, filter_: UserFilter) -> Sequence[User]: ...
