from typing import Protocol

from core.domain.lesson.dtos import GetLessonsReportDto
from core.models import LessonsReport


class LessonsReportQuery(Protocol):
    async def execute(self, dto: GetLessonsReportDto) -> LessonsReport:
        ...
