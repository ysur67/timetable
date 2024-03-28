from .base import Model
from .classroom import Classroom, ClassroomId
from .educational_level import EducationalLevel, EducationalLevelId
from .group import Group, GroupExternalId, GroupId, SimpleGroup
from .lesson import Lesson, LessonId
from .lessons_report import LessonsReport
from .subject import Subject, SubjectId
from .teacher import Teacher, TeacherId
from .user import User, UserId, UserPreferences, UserTelegramId

Group.model_rebuild()
Lesson.model_rebuild()
UserPreferences.model_rebuild()
LessonsReport.model_rebuild()

__all__ = [
    "Model",
    "EducationalLevel",
    "EducationalLevelId",
    "SimpleGroup",
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
    "User",
    "UserId",
    "UserTelegramId",
    "LessonsReport",
]
