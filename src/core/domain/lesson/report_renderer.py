from typing import Protocol, final

from jinja2 import Environment

from core.models.lessons_report import LessonsReport


class ReportRenderer(Protocol):
    async def render(self, report: LessonsReport) -> str: ...


@final
class JinjaReportRenderer(ReportRenderer):
    def __init__(self, env: Environment) -> None:
        self._env = env

    async def render(self, report: LessonsReport) -> str:
        template = self._env.get_template("lessons_report_message.jinja2")
        return await template.render_async(report=report)
