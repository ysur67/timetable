from collections.abc import Sequence
from datetime import date
from typing import Protocol

from pydantic import BaseModel

from core.models import Group, Lesson


class LessonsFilter(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    group: Group | None = None

    @property
    def has_any_value(self) -> bool:
        return (
            self.start_date is not None
            or self.end_date is not None
            or self.group is not None
        )

    @classmethod
    def empty(cls) -> "LessonsFilter":
        return cls()


class LessonRepository(Protocol):
    async def get(self, lesson: Lesson) -> Lesson | None:
        ...

    async def create(self, lesson: Lesson) -> Lesson:
        ...

    async def get_lessons(self, filter_: LessonsFilter) -> Sequence[Lesson]:
        ...
