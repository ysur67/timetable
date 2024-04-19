import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand
from core.domain.user.dtos import GetOrCreateUserDto
from core.impls.alchemy import tables
from core.models import User, UserTelegramId


async def test_command_will_create_new_user_if_there_is_no_such_telegram_id(
    get_or_create_user_command: GetOrCreateUserCommand,
    session: AsyncSession,
) -> None:
    dto = GetOrCreateUserDto(telegram_id=UserTelegramId(str(uuid.uuid4())))
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
    stmt = select(tables.User).where(tables.User.telegram_id == user_id)
    result = await session.scalars(stmt)
    records = result.all()
    users_count = len(records)
    return users_count > 0, users_count
