from typing import final

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core import models
from core.domain.lesson.repository import LessonRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.lesson import Lesson, UniqueLessonHashConstraint


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

    async def get_or_create(self, lesson: models.Lesson) -> tuple[models.Lesson, bool]:
        stmt = (
            insert(Lesson)
            .values(
                id=lesson.id,
                date_=lesson.date_,
                time_start=lesson.time_start,
                time_end=lesson.time_end,
                group_id=lesson.group.id,
                link=lesson.link,
                note=lesson.note,
                subject_id=lesson.subject.id if lesson.subject is not None else None,
                teacher_id=lesson.teacher.id if lesson.teacher is not None else None,
                classroom_id=lesson.classroom.id if lesson.classroom is not None else None,
                hash_=lesson.get_hash(),
            )
            .on_conflict_do_nothing(constraint=UniqueLessonHashConstraint)
            .options(
                selectinload(Lesson.group),
                selectinload(Lesson.classroom),
                selectinload(Lesson.subject),
                selectinload(Lesson.teacher),
            )
            .returning(Lesson)
        )
        await self._session.execute(stmt)
        return (lesson, True)
