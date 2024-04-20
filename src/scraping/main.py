import asyncio
import time

from di import create_container
from scraping.tasks.scrape_lessons import ScrapeLessonsTask


async def main() -> None:
    start = time.perf_counter()
    container = create_container()
    async with container.context() as context:
        task = await context.resolve(ScrapeLessonsTask)
        await task.scrape()
    print(f"new end: {time.perf_counter() - start}")  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
