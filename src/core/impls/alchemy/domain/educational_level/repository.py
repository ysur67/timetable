from collections.abc import Sequence
from typing import final

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import models
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.educational_level import EducationalLevel


@final
class AlchemyEducationalLevelRepository(EducationalLevelRepository):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
        from_domain_mapper: DomainToAlchemyMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper
        self._from_domain = from_domain_mapper

    async def get_all(self) -> Sequence[models.EducationalLevel]:
        stmt = select(EducationalLevel)
        result = await self._session.scalars(stmt)
        return [self._to_domain.map_educational_level(level) for level in result.all()]

    async def create(
        self,
        educational_level: models.EducationalLevel,
    ) -> models.EducationalLevel:
        model = self._from_domain.map_educational_level(educational_level)
        self._session.add(model)
        await self._session.flush()
        return educational_level
