import asyncio

from di import create_container
from scraping.scrapers.groups_scraper import GroupsScraper


async def main() -> None:
    container = create_container()
    async with container.context() as context:
        scraper = await context.resolve(GroupsScraper)
        await scraper.scrape()


if __name__ == "__main__":
    asyncio.run(main())
