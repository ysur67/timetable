import uuid

import factory
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.impls.alchemy import tables
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.models import Subject
from core.models.subject import SubjectId
from tests.factories.base import GenericFactory


class _SubjectFactory(GenericFactory[tables.Subject]):
    id = factory.LazyFunction(lambda: uuid.uuid4())
    title = factory.Faker("pystr")


class TestSubjectFactory:

    __test__ = False

    def __init__(self, session: AsyncSession, to_domain: AlchemyToDomainMapper) -> None:
        self._session = session
        self._to_domain = to_domain

    async def create(self) -> Subject:
        result = _SubjectFactory.build()
        self._session.add(result)
        await self._session.flush()
        return self._to_domain.map_subject(await self._get_subject(SubjectId(result.id)))

    async def create_batch(self, batch_size: int) -> list[Subject]:
        result = _SubjectFactory.build_batch(batch_size)
        self._session.add_all(result)
        await self._session.flush()
        db_subjects = await self._get_subjects([SubjectId(el.id) for el in result])
        return [self._to_domain.map_subject(subject) for subject in db_subjects]

    async def _get_subjects(self, ids: list[SubjectId]) -> list[tables.Subject]:
        stmt = select(tables.Subject).where(tables.Subject.id.in_(ids))
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def _get_subject(self, id_: SubjectId) -> tables.Subject:
        stmt = select(tables.Subject).where(tables.Subject.id == id_)
        result = await self._session.scalars(stmt)
        return result.one()
