from typing import Protocol, final

from jinja2 import Environment

from core.models import Lesson, SimpleGroup


class LessonsCreatedNotificationRenderer(Protocol):
    async def render(
        self,
        *,
        group: SimpleGroup,
        created_lessons: list[Lesson],
    ) -> str: ...


@final
class JinjaLessonsCreatedNotificationsRenderer(LessonsCreatedNotificationRenderer):
    def __init__(self, env: Environment) -> None:
        self._env = env

    async def render(
        self,
        *,
        group: SimpleGroup,
        created_lessons: list[Lesson],
    ) -> str:
        template = self._env.get_template("lessons_created_notification.jinja2")
        return await template.render_async(
            group=group,
            created_lessons=sorted(created_lessons, key=lambda lesson: lesson.date_),
        )


@final
class DummyLessonsCreatedNotificationsRenderer(LessonsCreatedNotificationRenderer):
    async def render(self, *, group: SimpleGroup, created_lessons: list[Lesson]) -> str:
        return group.title + " ".join([str(lesson.id) for lesson in created_lessons])
