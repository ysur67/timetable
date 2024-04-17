from collections.abc import Sequence
from typing import Protocol

from core.models.educational_level import EducationalLevelId
from core.models.group import Group


class SearchGroupsByTitleQuery(Protocol):
    async def execute(self, search_term: str, level_id: EducationalLevelId | None = None) -> Sequence[Group]: ...
