import uuid
from collections.abc import Sequence
from typing import Final, final

from faker import Faker
from neo4j import AsyncSession

from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models.educational_level import EducationalLevel
from scraping.clients.lessons.lessons_client import LessonsClient
from scraping.schemas.classroom import ClassroomSchema
from scraping.schemas.group import GroupWithoutCodeSchema
from scraping.schemas.lesson import LessonSchema
from scraping.schemas.subject import SubjectSchema
from scraping.schemas.teacher import TeacherSchema


@final
class DummyLessonsClient(LessonsClient):
    def __init__(
        self,
        size: int,
        session: AsyncSession,
        faker: Faker,
        mapper: NeoRecordToDomainMapper,
    ) -> None:
        self.size: Final = size
        self._session = session
        self._faker = faker
        self._mapper = mapper

    async def get_all(self, level: EducationalLevel) -> Sequence[LessonSchema]:
        stmt = """
            match (group:Group)-[:BELONGS_TO]-(educational_level:EducationalLevel)
                where educational_level.id = $level.id
            return group, educational_level;
        """
        result = await self._session.run(
            stmt,
            parameters={"level": level.model_dump(mode="json")},
        )
        record = await result.single()
        if record is None:
            return []
        group = self._mapper.map_group(record.data())
        return [
            LessonSchema(
                group=GroupWithoutCodeSchema(title=group.title),
                date_=self._faker.date(),
                starts_at=self._faker.time(),
                ends_at=self._faker.time(),
                classroom=ClassroomSchema(title=str(uuid.uuid4())),
                subject=SubjectSchema(title=str(uuid.uuid4())),
                teacher=TeacherSchema(name=str(uuid.uuid4())),
                note=self._faker.name(),
                href=self._faker.name(),
            )
            for _ in range(self.size)
        ]
