from collections.abc import Sequence
from typing import final

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import models
from core.domain.lesson.repository import LessonRepository, LessonsFilter
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.lesson import Lesson


@final
class AlchemyLessonRepository(LessonRepository):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
        from_domain_mapper: DomainToAlchemyMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper
        self._from_domain = from_domain_mapper

    async def get(self, lesson: models.Lesson) -> models.Lesson | None:
        stmt = (
            select(Lesson)
            .where(Lesson.hash_ == lesson.get_hash())
            .options(
                joinedload(Lesson.group),
                joinedload(Lesson.classroom),
                joinedload(Lesson.subject),
                joinedload(Lesson.teacher),
            )
        )
        model = await self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain.map_lesson(model)

    async def create(self, lesson: models.Lesson) -> models.Lesson:
        model = self._from_domain.map_lesson(lesson)
        self._session.add(model)
        await self._session.flush()
        return lesson

    async def get_lessons(self, filter_: LessonsFilter) -> Sequence[models.Lesson]:
        stmt = self._get_lessons_stmt(filter_)
        result = await self._session.scalars(stmt)
        return [self._to_domain.map_lesson(lesson) for lesson in result.all()]

    def _get_lessons_stmt(self, filter_: LessonsFilter) -> Select[tuple[Lesson]]:
        stmt = select(Lesson).options(
            joinedload(Lesson.group),
            joinedload(Lesson.classroom),
            joinedload(Lesson.subject),
            joinedload(Lesson.teacher),
        )
        if filter_.has_any_value is False:
            return stmt
        if filter_.start_date is not None:
            stmt = stmt.where(Lesson.date_ > filter_.start_date)
        if filter_.end_date is not None:
            stmt = stmt.where(Lesson.date_ < filter_.end_date)
        if filter_.group is not None:
            stmt = stmt.where(Lesson.group_id == filter_.group.id)
        return stmt
