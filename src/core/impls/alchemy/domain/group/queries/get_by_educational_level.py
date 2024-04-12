from collections.abc import Sequence
from typing import final

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import models
from core.domain.group.dtos import GetGroupsByEducationalLevelDto
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.tables import Group


@final
class AlchemyGetGroupsByEducationalLevelQuery(GetGroupsByEducationalLevelQuery):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper

    async def execute(
        self,
        dto: GetGroupsByEducationalLevelDto,
    ) -> Sequence[models.Group]:
        stmt = select(Group).where(Group.level_id == str(dto.level_id)).options(joinedload(Group.level))
        result = await self._session.scalars(stmt)
        return [self._to_domain.map_group(group) for group in result.all()]
