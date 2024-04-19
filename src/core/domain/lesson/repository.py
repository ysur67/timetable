from typing import Protocol

from core.models import Lesson


class LessonRepository(Protocol):
    async def get(self, lesson: Lesson) -> Lesson | None: ...

    async def create(self, lesson: Lesson) -> Lesson: ...

    async def get_or_create(self, lesson: Lesson) -> tuple[Lesson, bool]: ...
