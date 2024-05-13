from core.domain.lesson.repository import LessonRepository
from core.dtos import BaseDto
from core.models.lesson import Lesson


class DeleteOutdatedLessonsDto(BaseDto):
    existing_lessons: list[Lesson]


class DeleteOutdatedLessonsCommand:

    def __init__(self, lessons_repo: LessonRepository) -> None:
        self._lesson_repo = lessons_repo

    async def execute(self, dto: DeleteOutdatedLessonsDto) -> None:
        exiting_ids = [el.id for el in dto.existing_lessons]
        await self._lesson_repo.delete_outdated_ids(exiting_ids)
