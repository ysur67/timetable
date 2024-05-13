import uuid
from typing import Protocol

from pydantic import BaseModel

from core.models import Subject


class GetOrCreateSubjectParams(BaseModel):
    id: uuid.UUID
    title: str


class SubjectRepository(Protocol):
    async def get_by_title(self, title: str) -> Subject | None: ...

    async def create(self, subject: Subject) -> Subject: ...

    async def get_or_create(self, params: GetOrCreateSubjectParams) -> tuple[Subject, bool]: ...
