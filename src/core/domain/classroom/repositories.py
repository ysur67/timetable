from typing import Protocol

from core.models import Classroom


class ClassroomRepository(Protocol):
    async def get_by_title(self, title: str) -> Classroom | None:
        ...

    async def create(self, classroom: Classroom) -> Classroom:
        ...

    async def get_or_create(self, classroom: Classroom) -> Classroom:
        ...
