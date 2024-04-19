from pydantic import BaseModel

from core.models import EducationalLevelId


class EducationalLevelResponse(BaseModel):
    id: EducationalLevelId
    title: str
    code: str
