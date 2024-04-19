from datetime import date, time

from pydantic import BaseModel

from core.models.lesson import LessonId


class LessonResponse(BaseModel):
    id: LessonId
    date_: date
    time_start: time
    time_end: time
    note: str
    link: str
