import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.impls.alchemy.domain.educational_level.queries.get_all import (
    AlchemyGetAllEducationalLevelsQuery,
)
from core.impls.alchemy.domain.group.queries.get_by_educational_level import (
    AlchemyGetGroupsByEducationalLevelQuery,
)
from core.impls.alchemy.domain.lesson.queries.lessons_report import (
    AlchemyLessonsReportQuery,
)
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper


@pytest.fixture()
def get_all_educational_levels_query(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
) -> GetAllEducationalLevelsQuery:
    return AlchemyGetAllEducationalLevelsQuery(session, alchemy_to_domain_mapper)


@pytest.fixture()
def get_groups_by_educational_level_query(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
) -> GetGroupsByEducationalLevelQuery:
    return AlchemyGetGroupsByEducationalLevelQuery(session, alchemy_to_domain_mapper)


@pytest.fixture()
def get_lessons_report_query(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
) -> LessonsReportQuery:
    return AlchemyLessonsReportQuery(session, alchemy_to_domain_mapper)
