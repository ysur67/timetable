from core.domain.subject.repositories import SubjectRepository
from core.domain.subject.services import SubjectService
from core.models import Subject


class NeoSubjectService(SubjectService):
    def __init__(self, repo: SubjectRepository) -> None:
        self._repo = repo

    async def get_or_create(self, subject: Subject) -> Subject:
        result = await self._repo.get_by_title(subject.title)
        if result is not None:
            return result
        return await self._repo.create(subject)
