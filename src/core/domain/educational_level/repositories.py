from collections.abc import Sequence
from typing import Protocol

from core.models import EducationalLevel


class EducationalLevelRepository(Protocol):
    async def get_all(self) -> Sequence[EducationalLevel]:
        ...

    async def create(self, level: EducationalLevel) -> EducationalLevel:
        ...
