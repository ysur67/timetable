from typing import Protocol

from core.models.lesson import Lesson


class LessonService(Protocol):
    async def get_or_create(self, lesson: Lesson) -> Lesson:
        ...
