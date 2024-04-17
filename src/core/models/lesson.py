import hashlib
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
    group: "Group"
    teacher: "Teacher | None" = None
    subject: "Subject | None" = None
    classroom: "Classroom | None" = None
    link: str
    note: str

    def get_hash(self) -> str:
        subject = self.subject.title if self.subject is not None else "None"
        teacher = self.teacher.name if self.teacher is not None else "None"
        classroom = self.classroom.title if self.classroom is not None else "None"
        date_ = self.date_.isoformat()
        hash_ = hashlib.sha512(
            (
                self.group.title + subject + teacher + classroom + date_ + str(self.time_start) + str(self.time_end)
            ).encode(),
        )
        return hash_.hexdigest()
