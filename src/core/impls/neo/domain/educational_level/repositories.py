from collections.abc import Iterable
from typing import final

from neo4j import AsyncSession

from core.domain.educational_level.repositories import EducationalLevelRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models import EducationalLevel


@final
class NeoEducationalLevelRepository(EducationalLevelRepository):
    def __init__(
        self,
        session: AsyncSession,
        mapper: NeoRecordToDomainMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    async def get_all(self) -> Iterable[EducationalLevel]:
        stmt = """
            match (educational_level:EducationalLevel)
            return educational_level;
        """
        result = await self._session.run(stmt)
        records = await result.data()
        return [self._mapper.map_educational_level(level) for level in records]

    async def create(self, level: EducationalLevel) -> EducationalLevel:
        raise NotImplementedError
