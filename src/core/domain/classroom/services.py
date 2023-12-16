from typing import Protocol

from core.models import Classroom


class ClassroomService(Protocol):
    async def get_or_create(self, classroom: Classroom) -> Classroom:
        ...
