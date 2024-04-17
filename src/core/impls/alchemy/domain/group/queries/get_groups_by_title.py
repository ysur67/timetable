from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import models
from core.domain.group.queries.get_groups_by_title import SearchGroupsByTitleQuery
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.tables.group import Group
from core.models.educational_level import EducationalLevelId


class AlchemySearchGroupsByTitleQuery(SearchGroupsByTitleQuery):

    def __init__(self, session: AsyncSession, to_domain_mapper: AlchemyToDomainMapper) -> None:
        self._session = session
        self._to_domain = to_domain_mapper

    async def execute(self, search_term: str, level_id: EducationalLevelId | None = None) -> Sequence[models.Group]:
        if not search_term:
            return []
        stmt = select(Group)
        if level_id is not None:
            stmt = stmt.where(Group.level_id == level_id)
        stmt = stmt.where(Group.title.op("%")(search_term))
        results = await self._session.scalars(stmt)
        return [self._to_domain.map_group(el) for el in results.all()]
