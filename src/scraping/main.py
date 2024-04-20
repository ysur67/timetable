import asyncio

from di import create_container
from scraping.tasks.scrape_lessons import ScrapeLessonsTask


async def main() -> None:
    container = create_container()
    async with container.context() as context:
        task = await context.resolve(ScrapeLessonsTask)
        await task.scrape()


if __name__ == "__main__":
    asyncio.run(main())
