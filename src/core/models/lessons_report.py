from collections.abc import Sequence
from datetime import date

from core.models import Lesson, Model
from core.models.group import SimpleGroup


class LessonsReport(Model):
    lessons: Sequence[Lesson]
    group: SimpleGroup
    date_start: date
    date_end: date
