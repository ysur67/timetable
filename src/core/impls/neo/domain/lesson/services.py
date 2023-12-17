from typing import final

from core.domain.lesson.repository import LessonRepository
from core.domain.lesson.services import LessonService
from core.models.lesson import Lesson


@final
class NeoLessonService(LessonService):
    def __init__(self, repo: LessonRepository) -> None:
        self._repo = repo

    async def get_or_create(self, lesson: Lesson) -> Lesson:
        result = await self._repo.get(lesson)
        if result is not None:
            return result
        return await self._repo.create(lesson)
