from result import Err, Ok, Result

from core.domain.group.repositories import GroupRepository
from core.domain.user.dtos import SetSelectedGroupDto
from core.domain.user.repositories import UserRepository
from core.errors import EntityNotFoundError
from core.models import Group, GroupId
from core.models.user import UserPreferences


class SetSelectedGroupCommand:
    def __init__(
        self,
        user_repository: UserRepository,
        group_repository: GroupRepository,
    ) -> None:
        self._user_repository = user_repository
        self._group_repository = group_repository

    async def execute(
        self,
        dto: SetSelectedGroupDto,
    ) -> Result[Group, EntityNotFoundError[Group, GroupId]]:
        group = await self._group_repository.get_by_id(dto.group_id)
        if group is None:
            return Err(EntityNotFoundError(model=Group, id=dto.group_id))
        user = dto.user.model_copy(
            update={"preferences": UserPreferences(selected_group=group)},
        )
        await self._user_repository.save(user)
        return Ok(group)
