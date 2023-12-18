from collections.abc import Sequence
from typing import Protocol

from core.models import EducationalLevel


class GetAllEducationalLevelsQuery(Protocol):
    async def execute(self) -> Sequence[EducationalLevel]:
        ...
