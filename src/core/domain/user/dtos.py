from core.dtos import BaseDto
from core.models import UserTelegramId


class GetOrCreateUserDto(BaseDto):
    telegram_id: UserTelegramId
