from typing import final

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core import models
from core.domain.classroom.repositories import ClassroomRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.classroom import (
    Classroom,
    ClassroomUniqueTitleConstraint,
)


@final
class AlchemyClassroomRepository(ClassroomRepository):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
        from_domain_mapper: DomainToAlchemyMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper
        self._from_domain = from_domain_mapper

    async def get_by_title(self, title: str) -> models.Classroom | None:
        stmt = select(Classroom).where(
            func.lower(Classroom.title) == title.lower(),
        )
        result = await self._session.execute(stmt)
        model = result.scalar()
        if model is None:
            return None
        return self._to_domain.map_classroom(model)

    async def create(self, classroom: models.Classroom) -> models.Classroom:
        model = self._from_domain.map_classroom(classroom)
        self._session.add(model)
        await self._session.flush()
        return classroom

    async def get_or_create(
        self,
        classroom: models.Classroom,
    ) -> tuple[models.Classroom, bool]:
        stmt = (
            insert(Classroom)
            .values(id=classroom.id, title=classroom.title)
            .on_conflict_do_nothing(constraint=ClassroomUniqueTitleConstraint)
            .returning(Classroom)
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one()
        return (self._to_domain.map_classroom(row), True)
