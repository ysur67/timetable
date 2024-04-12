from collections.abc import Sequence
from datetime import date

from core.models import Lesson, Model
from core.models.group import Group


class LessonsReport(Model):
    lessons: Sequence[Lesson]
    group: Group
    date_start: date
    date_end: date
