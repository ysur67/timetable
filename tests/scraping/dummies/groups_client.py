import uuid
from collections.abc import Sequence
from typing import Final, final

from scraping.clients.groups.groups_client import GroupsClient
from scraping.schemas.educational_level import EducationalLevelSchema
from scraping.schemas.group import GroupSchema


@final
class DummyGroupsClient(GroupsClient):
    def __init__(self, response_size: int) -> None:
        self.size: Final = response_size

    async def get_all(
        self,
        level: EducationalLevelSchema,  # noqa: ARG002
    ) -> Sequence[GroupSchema]:
        return [GroupSchema(title=str(uuid.uuid4()), code=str(index)) for index in range(self.size)]
