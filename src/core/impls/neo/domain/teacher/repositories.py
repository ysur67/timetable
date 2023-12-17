from typing import final

from neo4j import AsyncSession

from core.domain.teacher.repositories import TeacherRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models import Teacher


@final
class NeoTeacherRepository(TeacherRepository):
    def __init__(
        self,
        session: AsyncSession,
        mapper: NeoRecordToDomainMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    async def get_by_name(self, name: str) -> Teacher | None:
        stmt = """
            match (teacher:Teacher)
                where teacher.name = $teacher
            return teacher;
        """
        result = await self._session.run(stmt, parameters={"teacher": name})
        record = await result.single()
        if record is None:
            return None
        return self._mapper.map_teacher(record.data())

    async def create(self, teacher: Teacher) -> Teacher:
        stmt = """
            create (teacher:Teacher {id: $teacher.id, name: $teacher.name});
        """
        await self._session.run(
            stmt,
            parameters={"teacher": teacher.model_dump(mode="json")},
        )
        return teacher
