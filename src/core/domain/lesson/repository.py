from datetime import date, time
from typing import Protocol

from pydantic import BaseModel

from core.models import Classroom, Group, Lesson, Subject, Teacher
from core.models.classroom import ClassroomId
from core.models.group import GroupId
from core.models.lesson import LessonId
from core.models.subject import SubjectId
from core.models.teacher import TeacherId


class GetOrCreateLessonParams(BaseModel):
    date_: date
    time_start: time
    time_end: time
    group: "Group"
    teacher: "Teacher | None" = None
    subject: "Subject | None" = None
    classroom: "Classroom | None" = None
    link: str
    note: str

    @property
    def group_id(self) -> GroupId:
        return self.group.id

    @property
    def teacher_id(self) -> TeacherId | None:
        if self.teacher is None:
            return None
        return self.teacher.id

    @property
    def subject_id(self) -> SubjectId | None:
        if self.subject is None:
            return None
        return self.subject.id

    @property
    def classroom_id(self) -> ClassroomId | None:
        if self.classroom is None:
            return None
        return self.classroom.id


class LessonRepository(Protocol):

    async def get(self, lesson: Lesson) -> Lesson | None: ...

    async def create(self, lesson: Lesson) -> Lesson: ...

    async def get_or_create(self, params: GetOrCreateLessonParams) -> tuple[Lesson, bool]: ...

    async def delete_outdated_ids(self, existing_ids: list[LessonId]) -> None: ...
