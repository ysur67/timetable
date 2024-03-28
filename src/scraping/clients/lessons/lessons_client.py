from collections.abc import Sequence
from typing import Protocol

from core.models.educational_level import EducationalLevel
from scraping.schemas import LessonSchema


class LessonsClient(Protocol):
    async def get_all(self, level: EducationalLevel) -> Sequence[LessonSchema]: ...
