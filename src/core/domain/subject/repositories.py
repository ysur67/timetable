from typing import Protocol

from core.models import Subject


class SubjectRepository(Protocol):
    async def get_by_title(self, title: str) -> Subject | None:
        ...

    async def create(self, subject: Subject) -> Subject:
        ...

    async def get_or_create(self, subject: Subject) -> Subject:
        ...
