import uuid
from typing import TYPE_CHECKING, NewType

if TYPE_CHECKING:
    from core.models.educational_level import EducationalLevelId


from core.models import Model

GroupId = NewType("GroupId", uuid.UUID)
GroupExternalId = NewType("GroupExternalId", str)


class SimpleGroup(Model):
    id: GroupId
    external_id: GroupExternalId
    title: str


class Group(Model):
    id: GroupId
    external_id: GroupExternalId
    title: str
    level_id: "EducationalLevelId"
