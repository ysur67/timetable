from collections.abc import Sequence
from datetime import date

from core.models import Group, Lesson, Model


class LessonsReport(Model):
    lessons: Sequence[Lesson]
    group: Group
    date_start: date
    date_end: date
