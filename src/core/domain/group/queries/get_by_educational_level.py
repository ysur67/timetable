from collections.abc import Sequence
from typing import Protocol

from core.domain.group.dtos import GetGroupsByEducationalLevelDto
from core.models import Group


class GetGroupsByEducationalLevelQuery(Protocol):
    async def execute(self, dto: GetGroupsByEducationalLevelDto) -> Sequence[Group]: ...
