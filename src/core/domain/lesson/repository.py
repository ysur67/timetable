from collections.abc import Sequence
from datetime import date
from typing import Protocol

from pydantic import BaseModel

from core.models import Lesson
from core.models.group import GroupId


class LessonsFilter(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    group_id: GroupId | None = None

    @property
    def has_any_value(self) -> bool:
        return (
            self.start_date is not None
            or self.end_date is not None
            or self.group_id is not None
        )

    @classmethod
    def empty(cls) -> "LessonsFilter":
        return cls()


class LessonRepository(Protocol):
    async def get(self, lesson: Lesson) -> Lesson | None: ...

    async def create(self, lesson: Lesson) -> Lesson: ...

    async def get_lessons(self, filter_: LessonsFilter) -> Sequence[Lesson]: ...

    async def get_or_create(self, lesson: Lesson) -> tuple[Lesson, bool]: ...
