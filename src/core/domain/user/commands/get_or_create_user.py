import uuid

from core.domain.user.dtos import GetOrCreateUserDto
from core.domain.user.repositories import UserRepository
from core.models import User
from core.models.user import UserId, UserPreferences


class GetOrCreateUserCommand:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repo = user_repository

    async def execute(self, dto: GetOrCreateUserDto) -> User:
        user = await self._user_repo.get_by_telegram_id(dto.telegram_id)
        if user is not None:
            return user
        return await self._user_repo.create(
            User(
                id=UserId(uuid.uuid4()),
                telegram_id=dto.telegram_id,
                preferences=UserPreferences.empty(),
            ),
        )
