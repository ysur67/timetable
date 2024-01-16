import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.domain.lesson.query.lessons_report import LessonsReportQuery
from core.domain.lesson.repository import LessonRepository
from core.impls.alchemy.domain.group.queries.get_by_educational_level import (
    AlchemyGetGroupsByEducationalLevelQuery,
)
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.neo.domain.educational_level.queries.get_all import (
    NeoGetAllEducationalLevelsQuery,
)
from core.impls.neo.domain.lesson.queries.lessons_report import NeoLessonsReportQuery


@pytest.fixture()
def get_all_educational_levels_query(
    educational_level_repository: EducationalLevelRepository,
) -> GetAllEducationalLevelsQuery:
    return NeoGetAllEducationalLevelsQuery(educational_level_repository)


@pytest.fixture()
def get_groups_by_educational_level_query(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
) -> GetGroupsByEducationalLevelQuery:
    return AlchemyGetGroupsByEducationalLevelQuery(session, alchemy_to_domain_mapper)


@pytest.fixture()
def get_lessons_report_query(lesson_repository: LessonRepository) -> LessonsReportQuery:
    return NeoLessonsReportQuery(lesson_repository)
