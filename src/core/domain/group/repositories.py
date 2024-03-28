from collections.abc import Iterable, Sequence
from typing import Protocol

from core.models.educational_level import EducationalLevelId
from core.models.group import Group, GroupId


class GroupRepository(Protocol):
    async def get_all(self) -> Iterable[Group]: ...

    async def get_by_educational_level(
        self,
        level_id: EducationalLevelId,
    ) -> Sequence[Group]: ...

    async def create_bulk(
        self,
        groups: Iterable[Group],
    ) -> Iterable[Group]: ...

    async def get_by_title(self, title: str) -> Group | None: ...

    async def get_by_id(self, ident: GroupId) -> Group | None: ...
