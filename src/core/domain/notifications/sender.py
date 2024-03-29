import asyncio
import collections
from typing import Protocol, final

from aiogram import Bot

from core.domain.user.repositories import UserFilter, UserRepository
from core.models import GroupId, User


class LessonsCreatedNotificationSender(Protocol):
    async def send(self, *, group_id: GroupId, message: str) -> None: ...


@final
class TelegramLessonsCreatedNotificationSender(LessonsCreatedNotificationSender):
    def __init__(self, bot: Bot, user_repo: UserRepository) -> None:
        self._bot = bot
        self._user_repo = user_repo

    async def send(self, *, group_id: GroupId, message: str) -> None:
        sem = asyncio.Semaphore(10)
        users = await self._user_repo.get_users(UserFilter(selected_group_id=group_id))
        tasks = [
            asyncio.create_task(
                self._send_message(
                    sem=sem,
                    user=user,
                    message=message,
                ),
            )
            for user in users
        ]
        await asyncio.gather(*tasks)

    async def _send_message(
        self,
        *,
        sem: asyncio.Semaphore,
        user: User,
        message: str,
    ) -> None:
        async with sem:
            await self._bot.send_message(
                user.telegram_id,
                message,
                parse_mode="HTML",
            )


@final
class DummyLessonsCreatedNotificationSender(LessonsCreatedNotificationSender):
    def __init__(self) -> None:
        self.sent_messages: dict[GroupId, list[str]] = collections.defaultdict(list)

    async def send(self, *, group_id: GroupId, message: str) -> None:
        self.sent_messages[group_id].append(message)
