import pytest
from neo4j import AsyncSession

from core.models.educational_level import EducationalLevel
from scraping.clients.groups_client import DummyGroupsClient
from scraping.scrapers.groups_scraper import GroupsScraper

pytestmark = [pytest.mark.anyio]


async def test_scrape_creates_actual_valid_data(
    groups_scraper: GroupsScraper,
    groups_client: DummyGroupsClient,
    educational_level: EducationalLevel,
    session: AsyncSession,
) -> None:
    count_before_execution = await _get_groups_count(session)
    await groups_scraper.scrape()
    count_after_execution = await _get_groups_count(session)
    assert count_after_execution > count_before_execution
    assert count_before_execution + groups_client.size == count_after_execution
    stmt = """
        match (g:Group)-[b:BELONGS_TO]-(e:EducationalLevel)
            where e.id = $level_id
        return count(*) as count;
    """
    result = await session.run(
        stmt,
        parameters={"level_id": str(educational_level.id)},
    )
    data = await result.single()
    assert data is not None
    assert data["count"] == groups_client.size


async def _get_groups_count(session: AsyncSession) -> int:
    stmt = """
        MATCH (:Group)
        RETURN count(*) as count;
    """
    result = await session.run(stmt)
    data = await result.single()
    assert data is not None
    return int(data["count"])
