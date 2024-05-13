import contextlib
from collections.abc import AsyncIterator, Iterable
from typing import Any

import aioinject
import httpx

from scraping.clients.groups.groups_client import GroupsClient
from scraping.clients.groups.http_client import HttpGroupsClient
from scraping.clients.lessons.http_client import HttpLessonsClient
from scraping.clients.lessons.lessons_client import LessonsClient
from scraping.scrapers.groups_scraper import GroupsScraper
from scraping.tasks import scrape_lessons
from scraping.tasks.scrape_lessons import ScrapeLessonsTask


@contextlib.asynccontextmanager
async def create_httpx_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(timeout=60) as client:
        yield client


providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Scoped(create_httpx_client),
    aioinject.Scoped(HttpGroupsClient, type_=GroupsClient),
    aioinject.Scoped(HttpLessonsClient, type_=LessonsClient),
    aioinject.Scoped(GroupsScraper),
    aioinject.Scoped(ScrapeLessonsTask),
    *scrape_lessons.providers,
]
