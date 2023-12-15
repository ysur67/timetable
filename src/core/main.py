import asyncio

import dotenv
from neo4j import AsyncSession

from di import create_container


async def main() -> None:
    container = create_container()
    async with container.context() as context:
        session = await context.resolve(AsyncSession)
        result = await session.run("return true;")
        data = await result.data()
        print(data)  # noqa: T201


if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    asyncio.run(main())
