import pytest

from core.domain.group.repositories import GroupRepository
from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand
from core.domain.user.commands.set_selected_group import SetSelectedGroupCommand
from core.domain.user.repositories import UserRepository


@pytest.fixture()
async def get_or_create_user_command(
    user_repository: UserRepository,
) -> GetOrCreateUserCommand:
    return GetOrCreateUserCommand(user_repository)


@pytest.fixture()
async def set_selected_group_command(
    user_repository: UserRepository,
    group_repository: GroupRepository,
) -> SetSelectedGroupCommand:
    return SetSelectedGroupCommand(user_repository, group_repository)
