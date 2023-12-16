import collections
from collections.abc import Iterable
from typing import final

from neo4j import AsyncSession

from core.domain.group.repositories import GroupRepository
from core.models import EducationalLevel, Group


@final
class NeoGroupRepository(GroupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> Iterable[Group]:
        stmt = """
            MATCH (group:Group)-[:BELONGS_TO]-(e:EducationalLevel)
            RETURN
                group.id as `id`,
                group.title as `title`,
                group.code as `code`,
                e.id as `educational_level_id`,
                e.title as `educational_level_title`,
                e.code as `educational_level_code`;
        """
        result = await self._session.run(stmt)
        groups = await result.data()
        return [
            Group(
                id=group["id"],
                external_id=group["code"],
                title=group["title"],
                level=EducationalLevel(
                    id=group["educational_level_id"],
                    title=group["educational_level_title"],
                    code=group["educational_level_code"],
                ),
            )
            for group in groups
        ]

    async def create_bulk(
        self,
        groups: Iterable[Group],
    ) -> Iterable[Group]:
        groups_by_level: dict[EducationalLevel, list[Group]]
        groups_by_level = collections.defaultdict(list)
        for group in groups:
            groups_by_level[group.level].append(group)
        for level, related_groups in groups_by_level.items():
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
                    "level_id": str(level.id),
                    "groups": [
                        group.model_dump(mode="json") for group in related_groups
                    ],
                },
            )
        return groups
