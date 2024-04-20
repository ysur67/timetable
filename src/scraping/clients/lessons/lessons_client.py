from collections.abc import Sequence
from datetime import date
from typing import Protocol

from core.models.educational_level import EducationalLevel
from scraping.schemas import LessonSchema


class LessonsClient(Protocol):

    async def get_all(self, level: EducationalLevel, *, start_date: date, end_date: date) -> Sequence[LessonSchema]: ...
