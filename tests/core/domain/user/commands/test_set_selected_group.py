import uuid

import pytest

from core.domain.user.commands.set_selected_group import SetSelectedGroupCommand
from core.domain.user.dtos import SetSelectedGroupDto
from core.errors import EntityNotFoundError
from core.models.group import Group, GroupId
from core.models.user import User

pytestmark = [pytest.mark.anyio]


async def test_returns_error_if_there_is_no_such_group(
    set_selected_group_command: SetSelectedGroupCommand,
    user: User,
) -> None:
    dto = SetSelectedGroupDto(user=user, group_id=GroupId(uuid.uuid4()))
    result = await set_selected_group_command.execute(dto)
    err = result.unwrap_err()
    assert isinstance(err, EntityNotFoundError)
    assert err.model is Group
    assert err.id == dto.group_id


async def test_returns_actual_group_if_there_is_such_group_id(
    set_selected_group_command: SetSelectedGroupCommand,
    user: User,
    group: Group,
) -> None:
    dto = SetSelectedGroupDto(user=user, group_id=group.id)
    result = await set_selected_group_command.execute(dto)
    group = result.unwrap()
    assert group.id == dto.group_id
