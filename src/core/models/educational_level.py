import uuid
from typing import NewType

from core.models import Model

EducationalLevelId = NewType("EducationalLevelId", uuid.UUID)


class EducationalLevel(Model):
    id: EducationalLevelId
    title: str
    code: str
