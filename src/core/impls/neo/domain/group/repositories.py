import collections
from collections.abc import Iterable, Sequence
from typing import final

from neo4j import AsyncSession

from core.domain.group.repositories import GroupRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models import Group
from core.models.educational_level import EducationalLevelId
from core.models.group import GroupId


@final
class NeoGroupRepository(GroupRepository):
    def __init__(
        self,
        session: AsyncSession,
        mapper: NeoRecordToDomainMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    async def get_all(self) -> Iterable[Group]:
        stmt = """
            MATCH (group:Group)-[:BELONGS_TO]-(educational_level:EducationalLevel)
            RETURN
                group,
                educational_level;
        """
        result = await self._session.run(stmt)
        records = await result.data()
        return [self._mapper.map_group(group) for group in records]

    async def create_bulk(
        self,
        groups: Iterable[Group],
    ) -> Iterable[Group]:
        groups_by_level: dict[EducationalLevelId, list[Group]]
        groups_by_level = collections.defaultdict(list)
        for group in groups:
            groups_by_level[group.level_id].append(group)
        for level_id, related_groups in groups_by_level.items():
            stmt = """
                MATCH (e:EducationalLevel)
                    WHERE e.id = $level_id
                FOREACH (group in $groups|
                    CREATE(
                        g:Group {
                            id: group.id,
                            title: group.title,
                            code: group.external_id
                        }
                    )-[:BELONGS_TO]->(e)
                )
            """
            await self._session.run(
                stmt,
                parameters={
                    "level_id": str(level_id),
                    "groups": [group.model_dump(mode="json") for group in related_groups],
                },
            )
        return groups

    async def get_by_title(self, title: str) -> Group | None:
        stmt = """
            MATCH (group:Group)-[:BELONGS_TO]-(educational_level:EducationalLevel)
                where toLower(group.title) = toLower($group)
            RETURN
                group,
                educational_level;
        """
        result = await self._session.run(stmt, parameters={"group": title})
        record = await result.single()
        if record is None:
            return None
        return self._mapper.map_group(record.data())

    async def get_by_educational_level(
        self,
        level_id: EducationalLevelId,
    ) -> Sequence[Group]:
        stmt = """
            MATCH (group:Group)-[:BELONGS_TO]-(educational_level:EducationalLevel)
                WHERE educational_level.id = $level_id
            RETURN
                group,
                educational_level;
        """
        result = await self._session.run(
            stmt,
            parameters={
                "level_id": str(level_id),
            },
        )
        records = await result.data()
        return [self._mapper.map_group(group) for group in records]

    async def get_by_id(self, ident: GroupId) -> Group | None:
        stmt = """
            MATCH (group:Group)-[:BELONGS_TO]-(educational_level:EducationalLevel)
                where group.id = $id
            RETURN
                group,
                educational_level;
        """
        result = await self._session.run(stmt, parameters={"id": str(ident)})
        record = await result.single()
        if record is None:
            return None
        return self._mapper.map_group(record.data())
