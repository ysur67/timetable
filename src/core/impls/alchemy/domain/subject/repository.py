from typing import final

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core import models
from core.domain.subject.repositories import SubjectRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.subject import Subject


@final
class AlchemySubjectRepository(SubjectRepository):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
        from_domain_mapper: DomainToAlchemyMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper
        self._from_domain = from_domain_mapper

    async def get_by_title(self, title: str) -> models.Subject | None:
        stmt = select(Subject).where(
            func.lower(Subject.title) == title.lower(),
        )
        model = await self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain.map_subject(model)

    async def create(self, subject: models.Subject) -> models.Subject:
        model = self._from_domain.map_subject(subject)
        self._session.add(model)
        await self._session.flush()
        return subject

    async def get_or_create(
        self,
        subject: models.Subject,
    ) -> tuple[models.Subject, bool]:
        model = await self.get_by_title(subject.title)
        if model is not None:
            return model, False
        return await self.create(subject), True
