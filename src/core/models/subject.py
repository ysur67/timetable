import uuid
from typing import NewType

from core.models import Model

SubjectId = NewType("SubjectId", uuid.UUID)


class Subject(Model):
    id: SubjectId
    title: str
