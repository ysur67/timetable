from neo4j import AsyncSession

from core.domain.classroom.repositories import ClassroomRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models import Classroom


class NeoClassroomRepository(ClassroomRepository):
    def __init__(self, session: AsyncSession, mapper: NeoRecordToDomainMapper) -> None:
        self._session = session
        self._mapper = mapper

    async def get_by_title(self, title: str) -> Classroom | None:
        stmt = """
            match (classroom:Classroom)
                where classroom.title = $classroom
            return classroom;
        """
        result = await self._session.run(stmt, parameters={"classroom": title})
        record = await result.single()
        if record is None:
            return None
        return self._mapper.map_classroom(record.data())

    async def create(self, classroom: Classroom) -> Classroom:
        stmt = """
            create (c:Classroom {id: $classroom.id, title: $classroom.title});
        """
        await self._session.run(
            stmt,
            parameters={"classroom": classroom.model_dump(mode="json")},
        )
        return classroom
