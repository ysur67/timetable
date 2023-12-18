from core.dtos import BaseDto
from core.models.educational_level import EducationalLevelId


class GetGroupsByEducationalLevelDto(BaseDto):
    level_id: EducationalLevelId
