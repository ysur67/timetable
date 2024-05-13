import operator
import re
from collections.abc import Sequence
from datetime import UTC, date, datetime, time
from functools import reduce
from typing import Final, final

import httpx
from pydantic import BaseModel
from selectolax.parser import HTMLParser, Node

from core.models.educational_level import EducationalLevel
from scraping.clients.lessons.lessons_client import LessonsClient
from scraping.schemas import LessonSchema
from scraping.schemas.classroom import ClassroomSchema
from scraping.schemas.group import GroupWithoutCodeSchema
from scraping.schemas.subject import SubjectSchema
from scraping.schemas.teacher import TeacherSchema


class _LessonsRequestParams(BaseModel):
    rtype: str = "3"
    ucstep: str
    """Код уровня образования"""
    exam: str = "0"
    datafrom: str
    dataend: str
    formo: str = "2"
    formob: str = "0"
    prdis: str = "0"

    @classmethod
    def date_to_request(cls, date_: date) -> str:
        return f"{date_.day}.{date_.month}.{date_.year}"


class InvalidLessonDateError(Exception):
    def __init__(self, date_string: str) -> None:
        super().__init__(
            f"'{date_string}' has invalid input format, parser can't handle it",
        )


class InvalidTimeRangeError(Exception):
    def __init__(self, value: str) -> None:
        super().__init__(f"Time range '{value}' has invalid format")


class InvalidTimeFormatError(Exception):
    def __init__(self, value: str) -> None:
        super().__init__(f"'{value} has invalid time format'")


# TODO: Переписать, своровано с прошлой имплементации
# https://github.com/ysur67/schedule/blob/master/apps/exchange/parse/http/lessons_main_site.py
@final
class HttpLessonsClient(LessonsClient):
    BASE_URL: Final = "http://inet.ibi.spb.ru/raspisan/rasp.php"

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_all(self, level: EducationalLevel, *, start_date: date, end_date: date) -> Sequence[LessonSchema]:
        result: list[LessonSchema] = []
        params = self._build_request_params(level, start_date=start_date, end_date=end_date)
        parser = await self._get_html_parser(params)
        for title_node in parser.tags("h4"):
            parent_center = title_node.parent
            if parent_center is None:
                continue
            table = parent_center.next
            if table is None or table.tag != "table":
                continue
            lesson_date = self._get_date_from_string(
                title_node.text(deep=False),
            )
            lessons = self._parse_lessons_table(table, lesson_date)
            result.extend(lessons)
        return result

    def _parse_lessons_table(
        self,
        table: Node,
        lesson_date: date,
    ) -> Sequence[LessonSchema]:
        if table.html is None:
            return []
        rows = table.css("tr")
        if len(rows) < 1:
            return []
        rows.pop(0)
        return reduce(
            operator.concat,
            [self._get_lesson_from_single_row(row, lesson_date) for row in rows],
        )

    def _get_lesson_from_single_row(
        self,
        row: Node,
        lesson_date: date,
    ) -> Sequence[LessonSchema]:
        if row.html is None:
            return []
        tds = row.css("td")
        if len(tds) < 1:
            return []
        # первый элемент - это номер строки
        tds.pop(0)
        groups_ind = 0
        lesson_schedule_ind = 1
        classroom_ind = 2
        subject_ind = 3
        teacher_ind = 4
        note_ind = 5
        groups = self._parse_groups(tds[groups_ind])
        if (
            time_range := self._get_time_range_from_string(
                tds[lesson_schedule_ind].text(deep=False),
            )
        ) is not None:
            starts, ends = time_range
        classroom = self._parse_classroom(tds[classroom_ind])
        subject: SubjectSchema | None = None
        href = ""
        if (subj_result := self._parse_subject(tds[subject_ind])) is not None:
            subject, href = subj_result
        teacher = self._parse_teacher(tds[teacher_ind])
        note = self._parse_note(tds[note_ind])
        return [
            LessonSchema(
                group=group,
                date_=lesson_date,
                starts_at=starts,
                ends_at=ends,
                classroom=classroom,
                subject=subject,
                teacher=teacher,
                note=note,
                href=href,
            )
            for group in groups
        ]

    def _parse_groups(self, cell: Node) -> Sequence[GroupWithoutCodeSchema]:
        titles = cell.text(deep=False).strip()
        return [GroupWithoutCodeSchema(title=title) for title in titles.split(",")]

    def _get_time_range_from_string(self, value: str) -> tuple[time, time] | None:
        """Получить временной диапазон из строки.
        Обязательный формат строки, который используется на данный момент
        `hh:mm-hh:mm`.

        Args:
            string (str): Строка с временным промежутком.

        Raises:
            TypeError: Если строка имеет неправильный формат.

        Returns:
            time, time: Диапазон, вида - начало, конец.
        """
        initial = value.split("-")
        if not initial:
            raise InvalidTimeRangeError(value)
        try:
            start_hour, start_minute = self._get_hours_and_minutes(initial[0])
        except InvalidTimeFormatError:
            return None
        try:
            end_hour, end_minute = self._get_hours_and_minutes(initial[1])
        except InvalidTimeFormatError:
            return None
        start = time(hour=start_hour, minute=start_minute)
        end = time(hour=end_hour, minute=end_minute)
        return start, end

    def _get_hours_and_minutes(self, value: str) -> tuple[int, int]:
        """Получить часы и минуты из строки.

        Обязательный формат строки - `hh:mm`

        Args:
            string (str): Строка

        Raises:
            TypeError: Если строка имеет неправильный формат.

        Returns:
            int, int: Часы, минуты.
        """
        initial = value.split(":")
        if not initial:
            raise InvalidTimeFormatError(value)
        hour = int(initial[0])
        minute = int(initial[1])
        return hour, minute

    def _parse_classroom(self, cell: Node) -> ClassroomSchema | None:
        title = cell.text(deep=False).strip()
        if not title:
            return None
        return ClassroomSchema(title=title)

    def _parse_subject(self, cell: Node) -> tuple[SubjectSchema, str] | None:
        title = cell.text(deep=False).strip()
        if not title:
            return None
        href = self._get_url_from_string(title)
        if href:
            title = title.replace(href, "")
        return (SubjectSchema(title=title), href)

    def _parse_teacher(self, cell: Node) -> TeacherSchema | None:
        name = cell.text(deep=False).strip()
        if not name:
            return None
        return TeacherSchema(name=name)

    def _parse_note(self, cell: Node) -> str:
        return cell.text(deep=False).strip()

    def _get_date_from_string(self, value: str) -> date:
        initial = value.split(" ")
        if not initial or len(initial) < 2:  # noqa: PLR2004
            raise InvalidLessonDateError(value)
        date_format = "%d.%m.%Y"
        return datetime.strptime(initial[0], date_format).replace(tzinfo=UTC).date()

    async def _get_html_parser(self, params: _LessonsRequestParams) -> HTMLParser:
        response = await self._client.post(
            self.BASE_URL,
            data=params.model_dump(mode="json"),
        )
        response.raise_for_status()
        return HTMLParser(response.text)

    def _build_request_params(
        self,
        level: EducationalLevel,
        *,
        start_date: date,
        end_date: date,
    ) -> _LessonsRequestParams:
        return _LessonsRequestParams(
            ucstep=level.code,
            datafrom=_LessonsRequestParams.date_to_request(start_date),
            dataend=_LessonsRequestParams.date_to_request(end_date),
        )

    def _get_url_from_string(self, value: str) -> str:
        values = re.findall(r"(https?://\S+)", value)
        return str(values[0]) if values else ""
