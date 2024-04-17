from core.domain.lesson.dtos import GetLessonsReportDto
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.domain.lesson.repository import LessonRepository
from core.models.lessons_report import LessonsReport


class NeoLessonsReportQuery(LessonsReportQuery):
    def __init__(self, repository: LessonRepository) -> None:
        self._repo = repository

    async def execute(self, dto: GetLessonsReportDto) -> LessonsReport:
        return LessonsReport(
            lessons=[],
            group=dto.group,
            date_start=dto.start_date,
            date_end=dto.end_date,
        )
