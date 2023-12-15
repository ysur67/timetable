import uuid
from typing import NewType

from core.models import Model

ClassroomId = NewType("ClassroomId", uuid.UUID)


class Classroom(Model):
    id: ClassroomId
    title: str
