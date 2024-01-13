from typing import final

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core import models
from core.domain.teacher.repositories import TeacherRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.teacher import Teacher


@final
class AlchemyTeacherRepository(TeacherRepository):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
        from_domain_mapper: DomainToAlchemyMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper
        self._from_domain = from_domain_mapper

    async def get_by_name(self, name: str) -> models.Teacher | None:
        stmt = select(Teacher).where(
            func.lower(Teacher.name) == name.lower(),
        )
        model = await self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain.map_teacher(model)

    async def create(self, teacher: models.Teacher) -> models.Teacher:
        model = self._from_domain.map_teacher(teacher)
        self._session.add(model)
        await self._session.flush()
        return teacher
