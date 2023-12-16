from collections.abc import Iterable
from typing import final

from neo4j import AsyncSession

from core.domain.educational_level.repositories import EducationalLevelRepository
from core.models import EducationalLevel


@final
class NeoEducationalLevelRepository(EducationalLevelRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> Iterable[EducationalLevel]:
        stmt = """
            match (level:EducationalLevel)
            return
                level.id as `id`,
                level.title as `title`,
                level.code as `code`;
        """
        result = await self._session.run(stmt)
        levels = await result.data()
        return [EducationalLevel.model_validate(el) for el in levels]

    async def create(self, level: EducationalLevel) -> EducationalLevel:
        raise NotImplementedError
