import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.impls.alchemy import tables
from scraping.scrapers.groups_scraper import GroupsScraper
from tests.scraping.dummies.groups_client import DummyGroupsClient

pytestmark = [pytest.mark.anyio]


async def test_scrape_creates_actual_valid_data(
    groups_scraper: GroupsScraper,
    groups_client: DummyGroupsClient,
    session: AsyncSession,
) -> None:
    count_before_execution = await _get_groups_count(session)
    await groups_scraper.scrape()
    count_after_execution = await _get_groups_count(session)
    assert count_after_execution > count_before_execution
    assert count_before_execution + groups_client.size == count_after_execution


async def _get_groups_count(session: AsyncSession) -> int:
    stmt = select(func.count()).select_from(tables.Group)
    result = (await session.execute(stmt)).one_or_none()
    assert result is not None
    return int(result.t[0])
