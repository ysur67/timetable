from typing import Protocol

from core.models import Teacher


class TeacherService(Protocol):
    async def get_or_create(self, teacher: Teacher) -> Teacher:
        ...
