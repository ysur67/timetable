from typing import Protocol

from pydantic import BaseModel

from core.models import Classroom


class GetOrCreateClassroomParams(BaseModel):
    title: str


class ClassroomRepository(Protocol):
    async def get_by_title(self, title: str) -> Classroom | None: ...

    async def create(self, classroom: Classroom) -> Classroom: ...

    async def get_or_create(self, params: GetOrCreateClassroomParams) -> tuple[Classroom, bool]: ...
