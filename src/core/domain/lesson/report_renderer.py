import asyncio
import collections
from collections.abc import Sequence
from datetime import date
from itertools import batched
from typing import Protocol, final

from jinja2 import Environment

from core.models.lesson import Lesson
from core.models.lessons_report import LessonsReport
from lib.dates import get_day_of_week


class ReportRenderer(Protocol):
    async def render(self, report: LessonsReport, days_per_message: int = 10) -> Sequence[str]: ...


@final
class JinjaReportRenderer(ReportRenderer):
    def __init__(self, env: Environment) -> None:
        self._env = env

    async def render(self, report: LessonsReport, days_per_message: int = 10) -> Sequence[str]:
        if len(report.lessons) == 0:
            template = self._env.get_template("empty_lessons_report_message.jinja2")
            return [await template.render_async(report=report)]
        template = self._env.get_template("lessons_report_message.jinja2")
        lessons_by_date: dict[date, list[Lesson]] = collections.defaultdict(list)
        for lesson in report.lessons:
            lessons_by_date[lesson.date_].append(lesson)
        batched_lessons_by_dates = list(batched(lessons_by_date.items(), days_per_message))
        tasks = [
            template.render_async(
                report=report,
                lessons_batch=batch,
                batch_index=batch_index,
                get_day_of_week=get_day_of_week,
            )
            for batch_index, batch in enumerate(batched_lessons_by_dates)
        ]
        return await asyncio.gather(*tasks)
