from collections.abc import Sequence
from typing import Protocol

from pydantic import BaseModel

from core.dtos import PaginationDto
from core.models.educational_level import EducationalLevelId
from core.models.group import Group
from core.types import Paginated


class GroupsFilter(BaseModel):
    search_term: str | None = None
    educational_level_id: EducationalLevelId | None = None


class GetGroupsQuery(Protocol):
    async def execute(self, filter_: GroupsFilter) -> Sequence[Group]: ...


class GetGroupsQueryPaginated(Protocol):
    async def execute(self, filter_: GroupsFilter, pagination: PaginationDto) -> Paginated[Group]: ...
