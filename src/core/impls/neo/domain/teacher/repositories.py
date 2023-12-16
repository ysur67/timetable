from typing import final

from neo4j import AsyncSession

from core.domain.teacher.repositories import TeacherRepository
from core.models import Subject, Teacher


@final
class NeoTeacherRepository(TeacherRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_name(self, name: str) -> Subject | None:
        stmt = """
            match (t:Teacher)
                where t.name = $teacher
            return t;
        """
        result = await self._session.run(stmt, parameters={"teacher": name})
        record = await result.single()
        if record is None:
            return None
        return Teacher(id=record["id"], name=record["name"])

    async def create(self, teacher: Teacher) -> Teacher:
        stmt = """
            create (t:Teacher {id: $teacher.id, name: $teacher.name});
        """
        await self._session.run(
            stmt,
            parameters={"teacher": teacher.model_dump(mode="json")},
        )
        return teacher
