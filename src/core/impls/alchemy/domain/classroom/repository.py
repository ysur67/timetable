import uuid
from typing import final

from sqlalchemy import Exists, func, literal, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from core import models
from core.domain.classroom.repositories import (
    ClassroomRepository,
    GetOrCreateClassroomParams,
)
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.classroom import (
    Classroom,
)
from core.models.classroom import ClassroomId


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

    async def get_or_create(self, params: GetOrCreateClassroomParams) -> tuple[models.Classroom, bool]:
        ident = self._generate_id()
        extant = aliased(Classroom, select(Classroom.id).where(Classroom.title == params.title).cte("extant"))
        inserted = aliased(
            Classroom,
            (
                insert(Classroom)
                .from_select(
                    ["id", "title"],
                    select(literal(ident).label("id"), literal(params.title).label("title")).where(~Exists(extant)),
                )
                .returning(Classroom)
                .cte("inserted")
            ),
        )
        stmt = select(inserted.id, literal(value=True).label("is_created")).union_all(
            select(extant.id, literal(value=False).label("is_created")),
        )
        ident, is_created = (await self._session.execute(stmt)).one()
        return (models.Classroom(id=ident, title=params.title), is_created)

    def _generate_id(self) -> ClassroomId:
        return ClassroomId(uuid.uuid4())
