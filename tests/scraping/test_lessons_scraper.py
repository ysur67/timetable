import pytest
from neo4j import AsyncSession

from scraping.scrapers.lessons_scraper import LessonsScraper
from tests.scraping.dummies.lessons_client import DummyLessonsClient

pytestmark = [pytest.mark.anyio]


@pytest.mark.usefixtures("group")
async def test_scraper_will_create_new_lessons(
    lessons_scraper: LessonsScraper,
    session: AsyncSession,
    lessons_client: DummyLessonsClient,
) -> None:
    count_before_execution = await _get_lessons_count(session)
    await lessons_scraper.scrape()
    count_after_execution = await _get_lessons_count(session)
    assert count_before_execution + lessons_client.size == count_after_execution


async def _get_lessons_count(session: AsyncSession) -> int:
    stmt = """
        MATCH (:Lesson)
        RETURN count(*) as count;
    """
    result = await session.run(stmt)
    data = await result.single()
    assert data is not None
    return int(data["count"])
