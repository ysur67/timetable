from typing import Protocol

from core.models import Subject


class SubjectService(Protocol):
    async def get_or_create(self, subject: Subject) -> Subject:
        ...
