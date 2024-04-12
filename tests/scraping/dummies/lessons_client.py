import uuid
from collections.abc import Sequence
from typing import Final, final

from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.impls.alchemy import tables
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
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
        mapper: AlchemyToDomainMapper,
    ) -> None:
        self.size: Final = size
        self._session = session
        self._faker = faker
        self._mapper = mapper

    async def get_all(self, level: EducationalLevel) -> Sequence[LessonSchema]:
        stmt = (
            select(tables.Group).where(tables.Group.level_id == str(level.id)).options(joinedload(tables.Group.level))
        )
        group_model = await self._session.scalar(stmt)
        if group_model is None:
            return []
        group = self._mapper.map_group(group_model)
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
