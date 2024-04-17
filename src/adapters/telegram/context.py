from pydantic import BaseModel

from core.models.educational_level import EducationalLevelId


class GroupSelectionContext(BaseModel):
    before_group_search_message_id: int | None = None
    educational_level_id: EducationalLevelId
