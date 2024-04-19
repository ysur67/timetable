import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.impls.alchemy import tables
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.models import EducationalLevel, Group
from core.models.lesson import Lesson
from core.models.user import User
from tests.factories.educational_level_factory import EducationalLevelFactory
from tests.factories.group_factory import GroupFactory
from tests.factories.lessons_factory import TestLessonFactory
from tests.factories.user_factory import UserFactory, UserPreferencesFactory


@pytest.fixture()
async def educational_level(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
) -> EducationalLevel:
    level = EducationalLevelFactory.build()
    session.add(level)
    await session.flush()
    return alchemy_to_domain_mapper.map_educational_level(level)


@pytest.fixture()
async def group(
    session: AsyncSession,
    educational_level: EducationalLevel,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
) -> Group:
    group = GroupFactory.build(level_id=str(educational_level.id))
    session.add(group)
    await session.flush()
    level = await session.get(tables.EducationalLevel, group.level_id)
    assert level is not None
    group.level = level
    return alchemy_to_domain_mapper.map_group(group)


@pytest.fixture()
async def user(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
) -> User:
    user = UserFactory.build()
    session.add(user)
    await session.flush()
    prefs = UserPreferencesFactory.build(user_id=user.id)
    session.add(prefs)
    await session.flush()
    user.preferences = prefs
    return alchemy_to_domain_mapper.map_user(user)


@pytest.fixture()
async def lesson(group: Group, lesson_factory: TestLessonFactory) -> Lesson:
    return await lesson_factory.create(group_id=group.id)
