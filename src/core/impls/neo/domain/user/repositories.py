from neo4j import AsyncSession

from core.domain.user.repositories import UserRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
from core.models.group import Group
from core.models.user import User, UserTelegramId


class NeoUserRepository(UserRepository):
    def __init__(self, session: AsyncSession, mapper: NeoRecordToDomainMapper) -> None:
        self._session = session
        self._mapper = mapper

    async def get_by_telegram_id(self, ident: UserTelegramId) -> User | None:
        stmt = """
            match (user:User)
                where user.telegram_id = $telegram_id
            optional match (user)-[:PICKED_SCHEDULE_OF]-(group:Group)-[:BELONGS_TO]-(educational_level:EducationalLevel)
            return user, group, educational_level;
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
        if (group := user.preferences.selected_group) is None:
            return user
        await self._create_selected_group_relationship(user, group)
        return user

    async def save(self, user: User) -> User:
        if (group := user.preferences.selected_group) is not None:
            await self._create_selected_group_relationship(user, group)
        else:
            await self._delete_selected_group_relationship(user)
        return user

    async def _delete_selected_group_relationship(self, user: User) -> None:
        stmt = """
            match (user:User)-[r:PICKED_SCHEDULE_OF]-(group:Group)
                where user.id = $user.id
            delete r;
        """
        await self._session.run(stmt, parameters={"user": user.model_dump(mode="json")})

    async def _create_selected_group_relationship(
        self,
        user: User,
        group: Group,
    ) -> None:
        create_relationship_stmt = """
            match
                (user:User {id: $user.id}),
                (group:Group {id: $group.id})
            create (user)-[:PICKED_SCHEDULE_OF]->(group)
        """
        await self._session.run(
            create_relationship_stmt,
            parameters={
                "user": user.model_dump(mode="json"),
                "group": group.model_dump(mode="json"),
            },
        )
