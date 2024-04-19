from datetime import date
from typing import Protocol

from pydantic import BaseModel

from core.dtos import PaginationDto
from core.models import GroupId, Lesson
from core.types import Paginated


class LessonsFilter(BaseModel):
    date_start: date | None = None
    date_end: date | None = None
    group_id: GroupId | None = None


class GetLessonsQuery(Protocol):
    async def execute(self, filter_: LessonsFilter, pagination: PaginationDto) -> Paginated[Lesson]: ...
