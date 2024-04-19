from collections.abc import Sequence
from typing import final

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core import models
from core.domain.group.queries.get_groups_query import (
    GetGroupsQuery,
    GetGroupsQueryPaginated,
    GroupsFilter,
)
from core.dtos import PaginationDto
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.tables import Group
from core.types import Paginated


@final
class AlchemyGetGroupsQuery(GetGroupsQuery):

    def __init__(self, session: AsyncSession, to_domain: AlchemyToDomainMapper) -> None:
        self._session = session
        self._to_domain = to_domain

    async def execute(self, filter_: GroupsFilter) -> Sequence[models.Group]:
        stmt = select(Group)
        if filter_.educational_level_id is not None:
            stmt = stmt.where(Group.level_id == filter_.educational_level_id)
        if filter_.search_term:
            stmt = stmt.where(Group.title.op("%")(filter_.search_term))
        results = await self._session.scalars(stmt)
        return [self._to_domain.map_group(el) for el in results.all()]


@final
class AlchemyGetGroupsQueryPaginated(GetGroupsQueryPaginated):
    def __init__(self, session: AsyncSession, to_domain: AlchemyToDomainMapper) -> None:
        self._session = session
        self._to_domain = to_domain

    async def execute(self, filter_: GroupsFilter, pagination: PaginationDto) -> Paginated[models.Group]:
        stmt = select(Group, func.count(Group.id).over().label("total_count"))
        if filter_.educational_level_id is not None:
            stmt = stmt.where(Group.level_id == filter_.educational_level_id)
        if filter_.search_term:
            stmt = stmt.where(Group.title.op("%")(filter_.search_term))
        stmt = stmt.limit(pagination.page_size)
        stmt = stmt.offset(pagination.get_offset())
        stmt = stmt.order_by(Group.id.desc())
        results = await self._session.execute(stmt)
        rows = results.tuples().all()
        if len(rows) == 0:
            return Paginated.empty(pagination.page)
        _, total_count = rows[0]
        groups = [self._to_domain.map_group(group) for (group, _) in rows]
        return Paginated(data=groups, current_page=pagination.page, total_count=total_count)
