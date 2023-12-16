from .base import Model
from .classroom import Classroom, ClassroomId
from .educational_level import EducationalLevel, EducationalLevelId
from .group import Group, GroupExternalId, GroupId
from .lesson import Lesson, LessonId
from .subject import Subject, SubjectId
from .teacher import Teacher, TeacherId

Group.model_rebuild()
Lesson.model_rebuild()

__all__ = [
    "Model",
    "EducationalLevel",
    "EducationalLevelId",
    "Group",
    "GroupId",
    "GroupExternalId",
    "Lesson",
    "LessonId",
    "Teacher",
    "TeacherId",
    "Classroom",
    "ClassroomId",
    "Subject",
    "SubjectId",
]
