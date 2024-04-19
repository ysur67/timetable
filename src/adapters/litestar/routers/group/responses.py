from pydantic import BaseModel

from core.models import EducationalLevelId, GroupId


class GroupResponse(BaseModel):
    id: GroupId
    title: str
    educational_level_id: EducationalLevelId
