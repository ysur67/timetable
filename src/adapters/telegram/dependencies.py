import contextlib
from collections.abc import AsyncIterator

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

from lib.settings import TelegramSettings


@contextlib.asynccontextmanager
async def create_bot(settings: TelegramSettings) -> AsyncIterator[Bot]:
    async with AiohttpSession() as session:
        yield Bot(token=settings.token, session=session)
