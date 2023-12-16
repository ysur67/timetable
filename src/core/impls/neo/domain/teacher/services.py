from core.domain.teacher.repositories import TeacherRepository
from core.domain.teacher.services import TeacherService
from core.models import Teacher


class NeoTeacherService(TeacherService):
    def __init__(self, repo: TeacherRepository) -> None:
        self._repo = repo

    async def get_or_create(self, teacher: Teacher) -> Teacher:
        result = await self._repo.get_by_name(teacher.title)
        if result is not None:
            return result
        return await self._repo.create(teacher)
