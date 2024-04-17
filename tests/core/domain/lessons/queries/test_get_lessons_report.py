from datetime import UTC, date, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.lesson.dtos import GetLessonsReportDto
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.models.group import Group
from core.models.lesson import Lesson
from tests.factories.lesson_factory import LessonFactory

pytestmark = [pytest.mark.anyio]


async def test_returns_actual_lesson_by_group(
    get_lessons_report_query: LessonsReportQuery,
    lesson: Lesson,
) -> None:
    result = await get_lessons_report_query.execute(
        GetLessonsReportDto(
            group=lesson.group,
            start_date=date.min,
            end_date=date.max,
        ),
        batch_size=10,
    )
    assert len(result.lessons[0]) == 1
    found = result.lessons[0][0]
    assert found.id == lesson.id
    assert lesson.group.id == found.group.id


async def test_returns_actual_lesson_filtered_by_dates(
    get_lessons_report_query: LessonsReportQuery,
    session: AsyncSession,
    group: Group,
) -> None:
    current_date = datetime.now(UTC).date()
    current_year_lessons = LessonFactory.build_batch(
        3,
        group_id=str(group.id),
        date_=current_date,
    )
    session.add_all(current_year_lessons)
    await session.flush()
    next_year_lessons = LessonFactory.build_batch(
        3,
        group_id=str(group.id),
        date_=current_date.replace(year=current_date.year + 1),
    )
    session.add_all(next_year_lessons)
    await session.flush()
    result = await get_lessons_report_query.execute(
        GetLessonsReportDto(
            start_date=current_date.replace(month=1, day=1),
            end_date=current_date.replace(month=12, day=31),
            group=group,
        ),
        batch_size=10,
    )

    assert len(result.lessons[0]) == len(current_year_lessons)
    current_year_ids = {lesson.id for lesson in current_year_lessons}
    for lesson in result.lessons[0]:
        assert lesson.id in current_year_ids
        assert lesson.date_.year == current_date.year

    result = await get_lessons_report_query.execute(
        GetLessonsReportDto(
            start_date=current_date.replace(year=current_date.year + 1, month=1, day=1),
            end_date=current_date.replace(year=current_date.year + 1, month=12, day=31),
            group=group,
        ),
        batch_size=10,
    )
    assert len(result.lessons[0]) == len(next_year_lessons)
    next_year_ids = {lesson.id for lesson in next_year_lessons}
    for lesson in result.lessons[0]:
        assert lesson.id in next_year_ids
        assert lesson.date_.year == current_date.year + 1
