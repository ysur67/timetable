from typing import final

from neo4j import AsyncSession

from core.domain.user.repositories import UserRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models.user import User, UserTelegramId


@final
class NeoUserRepository(UserRepository):
    def __init__(self, session: AsyncSession, mapper: NeoRecordToDomainMapper) -> None:
        self._session = session
        self._mapper = mapper

    async def get_by_telegram_id(self, ident: UserTelegramId) -> User | None:
        stmt = """
            match (user:User)
                where user.telegram_id = $telegram_id
            optional match (user)-[:PICKED_SCHEDULE_OF]-(group:Group)
            return user, group;
        """
        result = await self._session.run(stmt, parameters={"telegram_id": ident})
        record = await result.single()
        if record is None:
            return None
        return self._mapper.map_user(record.data())

    async def create(self, user: User) -> User:
        stmt = """
            create(user:User {id: $user.id, telegram_id: $user.telegram_id});
        """
        user_dict = user.model_dump(mode="json")
        await self._session.run(stmt, parameters={"user": user_dict})
        if user.preferences.selected_group is None:
            return user
        create_relationship_stmt = """
            match (user:User), (group:Group)
                where user.id = $user.id and group.id = $user.preferences.selected_group.id
            create((user)-[:PICKED_SCHEDULE_OF]->(group))
        """
        await self._session.run(
            create_relationship_stmt,
            parameters={"user": user_dict},
        )
        return user
