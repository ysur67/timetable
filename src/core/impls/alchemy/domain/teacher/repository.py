import uuid
from typing import final

from sqlalchemy import Exists, func, literal, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from core import models
from core.domain.teacher.repositories import GetOrCreateTeacherParams, TeacherRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.teacher import Teacher
from core.models.teacher import TeacherId


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

    async def get_or_create(
        self,
        params: GetOrCreateTeacherParams,
    ) -> tuple[models.Teacher, bool]:
        ident = self._generate_id()
        extant = aliased(Teacher, select(Teacher.id).where(Teacher.name == params.name).cte("extant"))
        inserted = aliased(
            Teacher,
            (
                insert(Teacher)
                .from_select(
                    ["id", "name"],
                    select(literal(ident).label("id"), literal(params.name).label("name")).where(~Exists(extant)),
                )
                .returning(Teacher)
                .cte("inserted")
            ),
        )
        stmt = select(inserted.id, literal(value=True).label("is_created")).union_all(
            select(extant.id, literal(value=False).label("is_created")),
        )
        ident, is_created = (await self._session.execute(stmt)).one()
        return (models.Teacher(id=ident, name=params.name), is_created)

    def _generate_id(self) -> TeacherId:
        return TeacherId(uuid.uuid4())
