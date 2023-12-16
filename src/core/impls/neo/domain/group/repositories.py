from collections.abc import Iterable
from typing import final

from neo4j import AsyncSession

from core.domain.group.repositories import GroupRepository
from core.models.educational_level import EducationalLevel
from core.models.group import Group


@final
class NeoGroupRepository(GroupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> Iterable[Group]:
        stmt = """
            MATCH (group:Group)-[:BELONGS_TO]-(e:EducationalLevel)
            RETURN
                group.id,
                group.title,
                group.code,
                e.id as `educational_level_id`,
                `e.title as `educational_level_title`,
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
        stmt = """
            FOREACH (group IN groups |
                MATCH (e:EducationalLevel)
                    WHERE e.id = group.level.id
                CREATE (
                    Group { id: group.id, title: group.title, code: group.code }-[:BELONGS_TO]->(e)
                )
            )
        """
        result = await self._session.run(stmt, groups=groups)
        data = await result.data()
        print(data)  # noqa: T201
        return groups
