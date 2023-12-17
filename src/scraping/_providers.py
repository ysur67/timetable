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
from scraping.scrapers.lessons_scraper import LessonsScraper


@contextlib.asynccontextmanager
async def create_httpx_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient() as client:
        yield client


providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Callable(create_httpx_client),
    aioinject.Callable(HttpGroupsClient, type_=GroupsClient),
    aioinject.Callable(HttpLessonsClient, type_=LessonsClient),
    aioinject.Callable(GroupsScraper),
    aioinject.Callable(LessonsScraper),
]
