from collections.abc import Sequence
from typing import final

from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.models import EducationalLevel


@final
class NeoGetAllEducationalLevelsQuery(GetAllEducationalLevelsQuery):
    def __init__(self, repository: EducationalLevelRepository) -> None:
        self._repo = repository

    async def execute(self) -> Sequence[EducationalLevel]:
        return await self._repo.get_all()
