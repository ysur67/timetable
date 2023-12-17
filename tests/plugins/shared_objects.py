import pytest
from neo4j import AsyncSession

from core.models import EducationalLevel, Group
from tests.factories.educational_level_factory import EducationalLevelFactory
from tests.factories.group_factory import GroupFactory


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
