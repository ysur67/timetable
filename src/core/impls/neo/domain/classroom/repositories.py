from typing import final

from neo4j import AsyncSession

from core.domain.classroom.repositories import ClassroomRepository
from core.models import Classroom


@final
class NeoClassroomRepository(ClassroomRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_title(self, title: str) -> Classroom | None:
        stmt = """
            match (c:Classroom)
                where c.title = $classroom
            return classroom;
        """
        result = await self._session.run(stmt, parameters={"classroom": title})
        record = await result.single()
        if record is None:
            return None
        return Classroom(id=record["id"], title=record["title"])

    async def create(self, classroom: Classroom) -> Classroom:
        stmt = """
            create (c:Classroom {id: $classroom.id, title: $classroom.title});
        """
        await self._session.run(
            stmt,
            parameters={"classroom": classroom.model_dump(mode="json")},
        )
        return classroom
