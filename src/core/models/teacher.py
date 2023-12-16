import uuid
from typing import NewType

from core.models import Model

TeacherId = NewType("TeacherId", uuid.UUID)


class Teacher(Model):
    id: TeacherId
    name: str
