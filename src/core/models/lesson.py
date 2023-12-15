import uuid
from datetime import date, time
from typing import TYPE_CHECKING, NewType

if TYPE_CHECKING:
    from core.models import Group, Subject, Teacher

from core.models import Model

LessonId = NewType("LessonId", uuid.UUID)


class Lesson(Model):
    id: LessonId
    title: str
    date_: date
    time_start: time
    time_end: time
    group: "Group"
    teacher: "Teacher | None"
    subject: "Subject"
    link: str
