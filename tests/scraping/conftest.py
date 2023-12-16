import pytest

from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from scraping.clients.groups_client import DummyGroupsClient
from scraping.scrapers.groups_scraper import GroupsScraper


@pytest.fixture()
def groups_client_response_size() -> int:
    return 10


@pytest.fixture()
def groups_client(groups_client_response_size: int) -> DummyGroupsClient:
    return DummyGroupsClient(groups_client_response_size)


@pytest.fixture()
def groups_scraper(
    groups_client: DummyGroupsClient,
    educational_level_repository: EducationalLevelRepository,
    group_repository: GroupRepository,
) -> GroupsScraper:
    return GroupsScraper(
        groups_client,
        educational_level_repository,
        group_repository,
    )
