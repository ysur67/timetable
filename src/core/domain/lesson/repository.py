from typing import Protocol

from core.models.lesson import Lesson


class LessonRepository(Protocol):
    async def get(self, lesson: Lesson) -> Lesson | None:
        ...

    async def create(self, lesson: Lesson) -> Lesson:
        ...
