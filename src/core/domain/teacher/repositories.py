from typing import Protocol

from core.models import Teacher


class TeacherRepository(Protocol):
    async def get_by_name(self, name: str) -> Teacher | None:
        ...

    async def create(self, teacher: Teacher) -> Teacher:
        ...

    async def get_or_create(self, teacher: Teacher) -> Teacher:
        ...
