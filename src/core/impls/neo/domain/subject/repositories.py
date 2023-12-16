from typing import final

from neo4j import AsyncSession

from core.domain.subject.repositories import SubjectRepository
from core.models import Subject


@final
class NeoSubjectRepository(SubjectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_title(self, title: str) -> Subject | None:
        stmt = """
            match (s:Subject)
                where s.title = $subject
            return s;
        """
        result = await self._session.run(stmt, parameters={"subject": title})
        record = await result.single()
        if record is None:
            return None
        return Subject(id=record["id"], title=record["title"])

    async def create(self, subject: Subject) -> Subject:
        stmt = """
            create (s:Subject {id: $subject.id, title: $subject.title});
        """
        await self._session.run(
            stmt,
            parameters={"subject": subject.model_dump(mode="json")},
        )
        return subject
