from typing import NewType

from core.models import Model

EducationalLevelId = NewType("EducationalLevelId", int)


class EducationalLevel(Model):
    id: EducationalLevelId
    title: str
    code: str
