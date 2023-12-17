from .base import BaseSchema
from .classroom import ClassroomSchema
from .educational_level import EducationalLevelSchema
from .group import GroupSchema, GroupWithoutCodeSchema
from .lesson import LessonSchema
from .subject import SubjectSchema
from .teacher import TeacherSchema

GroupSchema.model_rebuild()
LessonSchema.model_rebuild()

__all__ = [
    "BaseSchema",
    "ClassroomSchema",
    "SubjectSchema",
    "TeacherSchema",
    "EducationalLevelSchema",
    "GroupSchema",
    "GroupWithoutCodeSchema",
    "LessonSchema",
]
