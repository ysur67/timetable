from datetime import date

from core.dtos import BaseDto
from core.models.group import SimpleGroup


class GetLessonsReportDto(BaseDto):
    group: SimpleGroup
    start_date: date
    end_date: date
