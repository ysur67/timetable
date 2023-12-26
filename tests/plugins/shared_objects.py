import pytest
from neo4j import AsyncSession

from core.models import EducationalLevel, Group
from core.models.lesson import Lesson
from core.models.user import User
from tests.factories.educational_level_factory import EducationalLevelFactory
from tests.factories.group_factory import GroupFactory
from tests.factories.lesson_factory import LessonFactory
from tests.factories.user_factory import UserFactory
from tests.utils.models.lessons.create_lesson import create_lesson


@pytest.fixture()
async def educational_level(session: AsyncSession) -> EducationalLevel:
    stmt = """
        CREATE(e:EducationalLevel {id: $level.id, title: $level.title, code: $level.code})
    """
    level = EducationalLevelFactory.build()
    await session.run(stmt, parameters={"level": level.model_dump(mode="json")})
    return level


@pytest.fixture()
async def group(session: AsyncSession, educational_level: EducationalLevel) -> Group:
    stmt = """
        match (e:EducationalLevel)
        where e.id = $level.id
        CREATE(g:Group {id: $group.id, title: $group.title, code: $group.external_id})-[:BELONGS_TO]->(e)
    """
    group = GroupFactory.build(level=educational_level)
    await session.run(
        stmt,
        parameters={
            "group": group.model_dump(mode="json"),
            "level": educational_level.model_dump(mode="json"),
        },
    )
    return group


@pytest.fixture()
async def user(session: AsyncSession) -> User:
    stmt = """
        create (user:User {id: $user.id, telegram_id: $user.telegram_id});
    """
    user = UserFactory.build()
    await session.run(
        stmt,
        parameters={"user": user.model_dump(mode="json")},
    )
    return user


@pytest.fixture()
async def lesson(session: AsyncSession, group: Group) -> Lesson:
    return await create_lesson(session, LessonFactory.build(group=group))
