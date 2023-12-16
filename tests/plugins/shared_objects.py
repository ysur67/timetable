import pytest
from neo4j import AsyncSession

from core.models.educational_level import EducationalLevel
from tests.factories.educational_level_factory import EducationalLevelFactory


@pytest.fixture()
async def educational_level(session: AsyncSession) -> EducationalLevel:
    stmt = """
        CREATE(e:EducationalLevel {id: $level.id, title: $level.title, code: $level.code})
    """
    level = EducationalLevelFactory.build()
    await session.run(stmt, parameters={"level": level.model_dump(mode="json")})
    return level
