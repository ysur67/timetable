from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import models
from core.domain.user.repositories import UserRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper
from core.impls.alchemy.tables.group import Group
from core.impls.alchemy.tables.user import User, UserPreferences


class AlchemyUserRepository(UserRepository):
    def __init__(
        self,
        session: AsyncSession,
        to_domain_mapper: AlchemyToDomainMapper,
        from_domain_mapper: DomainToAlchemyMapper,
    ) -> None:
        self._session = session
        self._to_domain = to_domain_mapper
        self._from_domain = from_domain_mapper

    async def get_by_telegram_id(
        self,
        ident: models.UserTelegramId,
    ) -> models.User | None:
        stmt = (
            select(User)
            .where(User.telegram_id == ident)
            .options(
                joinedload(User.preferences)
                .joinedload(UserPreferences.selected_group)
                .joinedload(Group.level),
            )
        )
        model = await self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_domain.map_user(model)

    async def create(self, user: models.User) -> models.User:
        model = self._from_domain.map_user(user)
        self._session.add(model)
        await self._session.flush()
        return user

    async def save(self, user: models.User) -> models.User:
        # TODO: Разбить на set_
        group_id: str | None = None
        if user.preferences.selected_group is not None:
            group_id = str(user.preferences.selected_group.id)
        stmt = (
            update(UserPreferences)
            .where(
                UserPreferences.user_id == str(user.id),
            )
            .values(
                selected_group_id=str(group_id),
                report_days_offset=user.preferences.report_days_offset,
            )
        )
        await self._session.execute(stmt)
        await self._session.flush()
        return user
