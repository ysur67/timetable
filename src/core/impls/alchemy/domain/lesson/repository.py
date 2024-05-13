import uuid
from typing import final

from sqlalchemy import Exists, literal, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from core import models
from core.domain.lesson.repository import GetOrCreateLessonParams, LessonRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.lesson import Lesson
from core.models.lesson import LessonId


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

    async def get_or_create(self, params: GetOrCreateLessonParams) -> tuple[models.Lesson, bool]:
        ident = self._generate_id()
        lesson_hash = models.Lesson.create_hash(
            date_=params.date_,
            time_start=params.time_start,
            time_end=params.time_end,
            group=params.group,
            subject=params.subject,
            teacher=params.teacher,
            classroom=params.classroom,
        )
        extant = aliased(Lesson, select(Lesson.id).where(Lesson.hash_ == lesson_hash).cte("extant"))
        inserted = aliased(
            Lesson,
            (
                insert(Lesson)
                .from_select(
                    [
                        "id",
                        "hash_",
                        "group_id",
                        "classroom_id",
                        "subject_id",
                        "teacher_id",
                        "date_",
                        "time_start",
                        "time_end",
                        "link",
                        "note",
                    ],
                    select(
                        literal(ident).label("id"),
                        literal(lesson_hash).label("hash_"),
                        literal(params.group_id).label("group_id"),
                        literal(params.classroom_id).label("classroom_id"),
                        literal(params.subject_id).label("subject_id"),
                        literal(params.teacher_id).label("teacher_id"),
                        literal(params.date_).label("date_"),
                        literal(params.time_start).label("time_start"),
                        literal(params.time_end).label("time_end"),
                        literal(params.link).label("link"),
                        literal(params.note).label("note"),
                    ).where(~Exists(extant)),
                )
                .returning(Lesson)
                .cte("inserted")
            ),
        )
        stmt = select(inserted.id, literal(value=True).label("is_created")).union_all(
            select(extant.id, literal(value=False).label("is_created")),
        )
        ident, is_created = (await self._session.execute(stmt)).one()
        return (models.Lesson(id=ident, **params.model_dump()), is_created)

    def _generate_id(self) -> LessonId:
        return LessonId(uuid.uuid4())
