from typing import final

from core.domain.lesson.dtos import GetLessonsReportDto
from core.domain.lesson.query.lessons_report import LessonsReportQuery
from core.domain.lesson.repository import LessonRepository, LessonsFilter
from core.models.lessons_report import LessonsReport


@final
class NeoLessonsReportQuery(LessonsReportQuery):
    def __init__(self, repository: LessonRepository) -> None:
        self._repo = repository

    async def execute(self, dto: GetLessonsReportDto) -> LessonsReport:
        lessons = await self._repo.get_lessons(
            LessonsFilter(
                group=dto.group,
                start_date=dto.start_date,
                end_date=dto.end_date,
            ),
        )
        return LessonsReport(
            lessons=lessons,
            group=dto.group,
            date_start=dto.start_date,
            date_end=dto.end_date,
        )
