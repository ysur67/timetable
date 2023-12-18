import asyncio

from aiogram import Bot

from adapters.telegram.handlers import dispatcher
from di import create_container


async def main() -> None:
    container = create_container()
    async with container.context() as context:
        await run_bot(await context.resolve(Bot))


async def run_bot(bot: Bot) -> None:
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
