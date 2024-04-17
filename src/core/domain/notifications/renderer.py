import asyncio
from collections.abc import Sequence
from itertools import batched
from typing import Protocol, final

from jinja2 import Environment

from core.models import Group, Lesson
from lib.dates import get_day_of_week


class LessonsCreatedNotificationRenderer(Protocol):
    async def render(
        self,
        *,
        group: Group,
        created_lessons: list[Lesson],
    ) -> Sequence[str]: ...


@final
class JinjaLessonsCreatedNotificationsRenderer(LessonsCreatedNotificationRenderer):
    def __init__(self, env: Environment) -> None:
        self._env = env

    async def render(
        self,
        *,
        group: Group,
        created_lessons: list[Lesson],
    ) -> Sequence[str]:
        batch_size = 10
        template = self._env.get_template("lessons_created_notification.jinja2")
        batched_lessons = batched(sorted(created_lessons, key=lambda lesson: lesson.date_), batch_size)
        tasks = [
            template.render_async(
                group=group,
                created_lessons=batch,
                get_day_of_week=get_day_of_week,
            )
            for batch in batched_lessons
        ]
        return await asyncio.gather(*tasks)


@final
class DummyLessonsCreatedNotificationsRenderer(LessonsCreatedNotificationRenderer):
    async def render(self, *, group: Group, created_lessons: list[Lesson]) -> str:
        return group.title + " ".join([str(lesson.id) for lesson in created_lessons])
