from typing import Protocol

from pydantic import BaseModel

from core.models import Teacher


class GetOrCreateTeacherParams(BaseModel):
    name: str


class TeacherRepository(Protocol):
    async def get_by_name(self, name: str) -> Teacher | None: ...

    async def create(self, teacher: Teacher) -> Teacher: ...

    async def get_or_create(self, params: GetOrCreateTeacherParams) -> tuple[Teacher, bool]: ...
