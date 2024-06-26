from collections.abc import Iterable
from typing import Any

import aioinject
from jinja2 import Environment

from core.domain.lesson.commands.delete_outdated_lessons import (
    DeleteOutdatedLessonsCommand,
)
from core.domain.lesson.report_renderer import JinjaReportRenderer, ReportRenderer
from lib.jinja.templates import env

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Singleton(lambda: env, Environment),
    aioinject.Scoped(JinjaReportRenderer, ReportRenderer),
    aioinject.Scoped(DeleteOutdatedLessonsCommand),
]
