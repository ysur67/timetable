import uuid
from typing import TYPE_CHECKING, NewType

from core.models import Model

if TYPE_CHECKING:
    from core.models import Group


UserTelegramId = NewType("UserTelegramId", int)
UserId = NewType("UserId", uuid.UUID)


class UserPreferences(Model):
    selected_group: "Group | None" = None

    @classmethod
    def empty(cls) -> "UserPreferences":
        return UserPreferences()


class User(Model):
    id: UserId
    telegram_id: UserTelegramId
    preferences: UserPreferences
