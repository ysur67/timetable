from itertools import batched
from typing import final

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import models
from core.domain.lesson.dtos import GetLessonsReportDto
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.tables.lesson import Lesson
from core.models.lessons_report import LessonsReport


@final
class AlchemyLessonsReportQuery(LessonsReportQuery):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
    ) -> None:
        self._session = session
        self._to_domain_mapper = to_domain_mapper

    async def execute(self, dto: GetLessonsReportDto, batch_size: int) -> models.LessonsReport:
        stmt = (
            select(Lesson)
            .where(
                Lesson.group_id == str(dto.group.id),
                Lesson.date_ >= dto.start_date,
                Lesson.date_ <= dto.end_date,
            )
            .order_by(Lesson.date_)
            .options(
                joinedload(Lesson.group),
                joinedload(Lesson.classroom),
                joinedload(Lesson.subject),
                joinedload(Lesson.teacher),
            )
        )
        result = await self._session.scalars(stmt)
        rows = result.all()
        if len(rows) == 0:
            return LessonsReport(
                lessons=[],
                group=dto.group,
                date_start=dto.start_date,
                date_end=dto.end_date,
            )
        lessons = list(batched([self._to_domain_mapper.map_lesson(lesson) for lesson in rows], batch_size))
        return models.LessonsReport(
            lessons=lessons,
            group=dto.group,
            date_start=dto.start_date,
            date_end=dto.end_date,
        )
