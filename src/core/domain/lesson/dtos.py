from datetime import date

from core.dtos import BaseDto
from core.models import Group


class GetLessonsReportDto(BaseDto):
    group: Group
    start_date: date
    end_date: date
