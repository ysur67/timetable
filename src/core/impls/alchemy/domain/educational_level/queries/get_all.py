from collections.abc import Sequence
from typing import final

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.impls.alchemy import tables
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.models import EducationalLevel


@final
class AlchemyGetAllEducationalLevelsQuery(GetAllEducationalLevelsQuery):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper

    async def execute(self) -> Sequence[EducationalLevel]:
        stmt = select(tables.EducationalLevel)
        result = await self._session.scalars(stmt)
        return [self._to_domain.map_educational_level(level) for level in result.all()]
