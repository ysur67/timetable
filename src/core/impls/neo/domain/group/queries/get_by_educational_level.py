from collections.abc import Sequence

from core.domain.group.dtos import GetGroupsByEducationalLevelDto
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.domain.group.repositories import GroupRepository
from core.models import Group


class NeoGetGroupsByEducationalLevelQuery(GetGroupsByEducationalLevelQuery):
    def __init__(self, group_repository: GroupRepository) -> None:
        self._group_repository = group_repository

    async def execute(self, dto: GetGroupsByEducationalLevelDto) -> Sequence[Group]:
        return await self._group_repository.get_by_educational_level(dto.level_id)
