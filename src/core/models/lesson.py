import uuid
from datetime import date, time
from typing import TYPE_CHECKING, NewType

if TYPE_CHECKING:
    from core.models import Classroom, Group, Subject, Teacher

from core.models import Model

LessonId = NewType("LessonId", uuid.UUID)


class Lesson(Model):
    id: LessonId
    date_: date
    time_start: time
    time_end: time
    group: "Group | None"
    teacher: "Teacher | None"
    subject: "Subject | None"
    classroom: "Classroom | None"
    link: str
