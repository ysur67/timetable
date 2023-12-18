import pytest

from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand
from core.domain.user.repositories import UserRepository


@pytest.fixture()
async def get_or_create_user_command(
    user_repository: UserRepository,
) -> GetOrCreateUserCommand:
    return GetOrCreateUserCommand(user_repository)
