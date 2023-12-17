import asyncio

from di import create_container
from scraping.scrapers.groups_scraper import GroupsScraper
from scraping.scrapers.lessons_scraper import LessonsScraper


async def main() -> None:
    container = create_container()
    async with container.context() as context:
        groups_scraper = await context.resolve(GroupsScraper)
        await groups_scraper.scrape()
        lessons_scraper = await context.resolve(LessonsScraper)
        await lessons_scraper.scrape()


if __name__ == "__main__":
    asyncio.run(main())
