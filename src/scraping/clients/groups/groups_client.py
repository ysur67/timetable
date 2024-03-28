from collections.abc import Sequence
from typing import Protocol

from scraping.schemas.educational_level import EducationalLevelSchema
from scraping.schemas.group import GroupSchema


class GroupsClient(Protocol):
    async def get_all(self, level: EducationalLevelSchema) -> Sequence[GroupSchema]: ...
