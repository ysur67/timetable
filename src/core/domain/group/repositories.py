from collections.abc import Iterable
from typing import Protocol

from core.models import Group


class GroupRepository(Protocol):
    async def get_all(self) -> Iterable[Group]:
        ...

    async def create_bulk(
        self,
        groups: Iterable[Group],
    ) -> Iterable[Group]:
        ...
