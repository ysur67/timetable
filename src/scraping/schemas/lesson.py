from datetime import date, time
from typing import TYPE_CHECKING

from scraping.schemas.base import BaseSchema

if TYPE_CHECKING:
    from scraping.schemas import (
        ClassroomSchema,
        GroupWithoutCodeSchema,
        SubjectSchema,
        TeacherSchema,
    )


class LessonSchema(BaseSchema):
    group: "GroupWithoutCodeSchema"
    date_: date
    starts_at: time
    ends_at: time
    classroom: "ClassroomSchema | None"
    subject: "SubjectSchema | None"
    teacher: "TeacherSchema | None"
    note: str
    href: str
