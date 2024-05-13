import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.impls.alchemy import tables
from tests.scraping.dummies.lessons_client import DummyLessonsClient


@pytest.mark.usefixtures("group")
@pytest.mark.xfail("NotImplementedError")
async def test_scraper_will_create_new_lessons(
    session: AsyncSession,
    lessons_client: DummyLessonsClient,
) -> None:
    raise NotImplementedError
    count_before_execution = await _get_lessons_count(session)  # type: ignore[unreachable]
    # await lessons_scraper.scrape()  # noqa: ERA001
    count_after_execution = await _get_lessons_count(session)
    assert count_before_execution + lessons_client.size == count_after_execution


async def _get_lessons_count(session: AsyncSession) -> int:
    stmt = select(func.count()).select_from(tables.Lesson)
    result = (await session.execute(stmt)).one_or_none()
    assert result is not None
    return int(result[0])
