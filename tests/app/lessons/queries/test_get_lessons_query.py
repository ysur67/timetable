from core.domain.lesson.queries.get_lessons_query import GetLessonsQuery, LessonsFilter
from core.dtos import PaginationDto
from core.models import Group
from lib.dates import utc_now
from tests.app.utils.lessons import TestLessonFactory


async def test_returns_empty_object_if_there_are_no_lessons(get_lessons_query: GetLessonsQuery) -> None:
    result = await get_lessons_query.execute(LessonsFilter(), PaginationDto(page=1, page_size=10))
    assert result.total_count == 0
    assert len(result.data) == 0


async def test_returns_actual_lessons_if_there_are_any(
    get_lessons_query: GetLessonsQuery,
    lesson_factory: TestLessonFactory,
    group: Group,
) -> None:
    lessons = await lesson_factory.create_batch(20, group_id=group.id, date_=utc_now().date())
    page_size = 10
    result = await get_lessons_query.execute(
        LessonsFilter(group_id=group.id),
        pagination=PaginationDto(page=1, page_size=page_size),
    )
    assert result.total_count == len(lessons)
    assert len(result.data) == page_size
    assert all(lesson.group.id == group.id for lesson in result.data)
