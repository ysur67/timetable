from typing import final

from neo4j import AsyncSession

from core.domain.subject.repositories import SubjectRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models import Subject


@final
class NeoSubjectRepository(SubjectRepository):
    def __init__(
        self,
        session: AsyncSession,
        mapper: NeoRecordToDomainMapper,
    ) -> None:
        self._session = session
        self._mapper = mapper

    async def get_by_title(self, title: str) -> Subject | None:
        stmt = """
            match (subject:Subject)
                where subject.title = $subject
            return subject;
        """
        result = await self._session.run(stmt, parameters={"subject": title})
        record = await result.single()
        if record is None:
            return None
        return self._mapper.map_subject(record.data())

    async def create(self, subject: Subject) -> Subject:
        stmt = """
            create (subject:Subject {id: $subject.id, title: $subject.title});
        """
        await self._session.run(
            stmt,
            parameters={"subject": subject.model_dump(mode="json")},
        )
        return subject
