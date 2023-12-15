import uuid
from typing import TYPE_CHECKING, NewType

if TYPE_CHECKING:
    from core.models import EducationalLevel

from core.models import Model

GroupId = NewType("GroupId", uuid.UUID)


class Group(Model):
    id: GroupId
    title: str
    level: "EducationalLevel"
