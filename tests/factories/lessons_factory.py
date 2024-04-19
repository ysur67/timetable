import uuid
from datetime import UTC, date, datetime

import factory
from factory.fuzzy import FuzzyDate, FuzzyDateTime
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.impls.alchemy import tables
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.models.group import GroupId
from core.models.lesson import Lesson, LessonId
from tests.factories.base import GenericFactory


class _LessonFactory(GenericFactory[tables.Lesson]):
    id = factory.LazyFunction(lambda: uuid.uuid4())
    date_ = FuzzyDate(start_date=date.min)
    time_start = factory.LazyAttribute(
        lambda _: FuzzyDateTime(start_dt=datetime(1970, 1, 1, tzinfo=UTC)).fuzz().time(),
    )
    time_end = factory.LazyAttribute(
        lambda _: FuzzyDateTime(start_dt=datetime(1970, 1, 1, tzinfo=UTC)).fuzz().time(),
    )
    link = factory.Faker("pystr")
    note = factory.Faker("pystr")
    hash_ = factory.Faker("uuid4")


class TestLessonFactory:

    __test__ = False

    def __init__(self, session: AsyncSession, to_domain: AlchemyToDomainMapper) -> None:
        self._session = session
        self._to_domain = to_domain

    async def create(self, *, group_id: GroupId) -> Lesson:
        result = _LessonFactory.build(group_id=group_id)
        self._session.add(result)
        await self._session.flush()
        return self._to_domain.map_lesson(await self._get_lesson(LessonId(result.id)))

    async def create_batch(
        self,
        batch_size: int,
        *,
        group_id: GroupId,
        date_: date,
    ) -> list[Lesson]:
        result = _LessonFactory.build_batch(batch_size, group_id=group_id, date_=date_)
        self._session.add_all(result)
        await self._session.flush()
        db_lessons = await self._get_lessons([LessonId(el.id) for el in result])
        return [self._to_domain.map_lesson(lesson) for lesson in db_lessons]

    async def _get_lessons(self, ids: list[LessonId]) -> list[tables.Lesson]:
        stmt = self._lesson_stmt().where(tables.Lesson.id.in_(ids))
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def _get_lesson(self, id_: LessonId) -> tables.Lesson:
        stmt = self._lesson_stmt().where(tables.Lesson.id == id_)
        result = await self._session.scalars(stmt)
        return result.one()

    def _lesson_stmt(self) -> Select[tuple[tables.Lesson]]:
        return select(tables.Lesson).options(
            joinedload(tables.Lesson.group),
            joinedload(tables.Lesson.subject),
            joinedload(tables.Lesson.classroom),
            joinedload(tables.Lesson.teacher),
        )
