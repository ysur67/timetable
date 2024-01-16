from collections.abc import Iterable, Sequence
from typing import final

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import models
from core.domain.group.repositories import GroupRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.group import Group
from core.models.educational_level import EducationalLevelId


@final
class AlchemyGroupRepository(GroupRepository):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
        from_domain_mapper: DomainToAlchemyMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper
        self._from_domain = from_domain_mapper

    async def get_all(self) -> Iterable[models.Group]:
        stmt = select(Group).options(joinedload(Group.level))
        result = await self._session.scalars(stmt)
        return [self._to_domain.map_group(group) for group in result.all()]

    async def get_by_educational_level(
        self,
        level_id: EducationalLevelId,
    ) -> Sequence[models.Group]:
        stmt = (
            select(Group)
            .where(Group.level_id == level_id)
            .options(joinedload(Group.level))
        )
        result = await self._session.scalars(stmt)
        return [self._to_domain.map_group(group) for group in result.all()]

    async def create_bulk(
        self,
        groups: Iterable[models.Group],
    ) -> Iterable[models.Group]:
        models = [self._from_domain.map_group(group) for group in groups]
        self._session.add_all(models)
        await self._session.flush()
        return groups

    async def get_by_title(self, title: str) -> models.Group | None:
        stmt = (
            select(Group)
            .where(func.lower(Group.title) == title.lower())
            .options(joinedload(Group.level))
        )
        model = await self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain.map_group(model)

    async def get_by_id(self, ident: models.GroupId) -> models.Group | None:
        model = await self._session.get(
            Group,
            str(ident),
            options=[
                joinedload(Group.level),
            ],
        )
        if model is None:
            return None
        return self._to_domain.map_group(model)
