import contextlib
from collections.abc import AsyncIterator, Iterable
from typing import Any

import aioinject
import httpx

from scraping.clients.groups_client import GroupsClient, HttpGroupsClient
from scraping.scrapers.groups_scraper import GroupsScraper


@contextlib.asynccontextmanager
async def create_httpx_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient() as client:
        yield client


providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Callable(create_httpx_client),
    aioinject.Callable(HttpGroupsClient, type_=GroupsClient),
    aioinject.Callable(GroupsScraper),
]
