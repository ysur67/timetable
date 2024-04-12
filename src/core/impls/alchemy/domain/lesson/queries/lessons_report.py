from typing import final

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import models
from core.domain.lesson.dtos import GetLessonsReportDto
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.tables.lesson import Lesson


@final
class AlchemyLessonsReportQuery(LessonsReportQuery):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
    ) -> None:
        self._session = session
        self._to_domain_mapper = to_domain_mapper

    async def execute(self, dto: GetLessonsReportDto) -> models.LessonsReport:
        stmt = (
            select(Lesson)
            .where(
                Lesson.group_id == str(dto.group.id),
                Lesson.date_ >= dto.start_date,
                Lesson.date_ <= dto.end_date,
            )
            .options(
                joinedload(Lesson.group),
                joinedload(Lesson.classroom),
                joinedload(Lesson.subject),
                joinedload(Lesson.teacher),
            )
        )
        result = await self._session.scalars(stmt)
        return models.LessonsReport(
            lessons=[self._to_domain_mapper.map_lesson(lesson) for lesson in result.all()],
            group=dto.group,
            date_start=dto.start_date,
            date_end=dto.end_date,
        )
