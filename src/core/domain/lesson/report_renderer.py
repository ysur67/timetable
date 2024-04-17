import asyncio
from collections.abc import Sequence
from itertools import batched
from typing import Protocol, final

from jinja2 import Environment

from core.models.lessons_report import LessonsReport
from lib.dates import get_day_of_week


class ReportRenderer(Protocol):
    async def render(self, report: LessonsReport, batch_size: int = 10) -> Sequence[str]: ...


@final
class JinjaReportRenderer(ReportRenderer):
    def __init__(self, env: Environment) -> None:
        self._env = env

    async def render(self, report: LessonsReport, batch_size: int = 10) -> Sequence[str]:
        if len(report.lessons) == 0:
            template = self._env.get_template("empty_lessons_report_message.jinja2")
            return [await template.render_async(report=report)]
        template = self._env.get_template("lessons_report_message.jinja2")
        batched_lessons = list(batched(report.lessons, batch_size))
        tasks = [
            template.render_async(
                report=report,
                lessons_batch=batch,
                batch_index=batch_index,
                get_day_of_week=get_day_of_week,
            )
            for batch_index, batch in enumerate(batched_lessons)
        ]
        return await asyncio.gather(*tasks)
