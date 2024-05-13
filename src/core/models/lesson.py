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

    @classmethod
    def create_hash(
        cls,
        *,
        date_: date,
        time_start: time,
        time_end: time,
        group: "Group",
        subject: "Subject | None" = None,
        teacher: "Teacher | None" = None,
        classroom: "Classroom | None" = None,
    ) -> str:
        return cls._build_hash(
            date_=date_,
            time_start=time_start,
            time_end=time_end,
            group=group,
            subject=subject,
            teacher=teacher,
            classroom=classroom,
        )

    @classmethod
    def _build_hash(
        cls,
        *,
        date_: date,
        time_start: time,
        time_end: time,
        group: "Group",
        subject: "Subject | None" = None,
        teacher: "Teacher | None" = None,
        classroom: "Classroom | None" = None,
    ) -> str:
        subject_title = subject.title if subject is not None else "None"
        teacher_name = teacher.name if teacher is not None else "None"
        classroom_title = classroom.title if classroom is not None else "None"
        date_iso = date_.isoformat()
        hash_ = hashlib.sha512(
            (
                group.title
                + subject_title
                + teacher_name
                + classroom_title
                + date_iso
                + str(time_start)
                + str(time_end)
            ).encode(),
        )
        return hash_.hexdigest()

    def get_hash(self) -> str:
        return self._build_hash(
            date_=self.date_,
            time_start=self.time_start,
            time_end=self.time_end,
            group=self.group,
            subject=self.subject,
            teacher=self.teacher,
            classroom=self.classroom,
        )
