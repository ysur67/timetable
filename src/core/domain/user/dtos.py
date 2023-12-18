from core.dtos import BaseDto
from core.models import GroupId, User, UserTelegramId


class GetOrCreateUserDto(BaseDto):
    telegram_id: UserTelegramId


class SetSelectedGroupDto(BaseDto):
    group_id: GroupId
    user: User
