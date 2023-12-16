from core.domain.classroom.repositories import ClassroomRepository
from core.domain.classroom.services import ClassroomService
from core.models import Classroom


class NeoClassroomService(ClassroomService):
    def __init__(self, repo: ClassroomRepository) -> None:
        self._repo = repo

    async def get_or_create(self, classroom: Classroom) -> Classroom:
        result = await self._repo.get_by_title(classroom.title)
        if result is not None:
            return result
        return await self._repo.create(classroom)
