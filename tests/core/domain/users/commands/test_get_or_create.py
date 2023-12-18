import sys

import pytest
from neo4j import AsyncSession

from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand
from core.domain.user.dtos import GetOrCreateUserDto
from core.models import User, UserTelegramId

pytestmark = [pytest.mark.anyio]


async def test_command_will_create_new_user_if_there_is_no_such_telegram_id(
    get_or_create_user_command: GetOrCreateUserCommand,
    session: AsyncSession,
) -> None:
    dto = GetOrCreateUserDto(telegram_id=sys.maxsize)
    exists, _ = await _get_user_exists(session, dto.telegram_id)
    assert exists is False
    await get_or_create_user_command.execute(dto)
    exists, count = await _get_user_exists(session, dto.telegram_id)
    assert exists is True
    assert count == 1


async def test_will_not_create_user_if_such_telegram_id_already_exists(
    get_or_create_user_command: GetOrCreateUserCommand,
    session: AsyncSession,
    user: User,
) -> None:
    dto = GetOrCreateUserDto(telegram_id=user.telegram_id)
    exists, count = await _get_user_exists(session, dto.telegram_id)
    assert exists is True
    assert count == 1
    await get_or_create_user_command.execute(dto)
    exists, count = await _get_user_exists(session, dto.telegram_id)
    assert exists is True
    assert count == 1


async def _get_user_exists(
    session: AsyncSession,
    user_id: UserTelegramId,
) -> tuple[bool, int]:
    stmt = """
        match (user:User)
            where user.telegram_id = $user_id
        return user, count(*) as count;
    """
    result = await session.run(stmt, parameters={"user_id": user_id})
    record = await result.single()
    if record is None:
        return (False, 0)
    data = record.data()
    return (True, int(data["count"]))
