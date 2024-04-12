import collections

from core.domain.notifications.renderer import LessonsCreatedNotificationRenderer
from core.domain.notifications.sender import LessonsCreatedNotificationSender
from core.models import Group, Lesson


class SendLessonsCreatedNotificationCommand:
    def __init__(
        self,
        notification_renderer: LessonsCreatedNotificationRenderer,
        notification_sender: LessonsCreatedNotificationSender,
    ) -> None:
        self._notification_renderer = notification_renderer
        self._notification_sender = notification_sender

    async def execute(self, created_lessons: list[Lesson]) -> None:
        if not created_lessons:
            return

        lessons_by_group: dict[Group, list[Lesson]] = collections.defaultdict(
            list,
        )
        for lesson in created_lessons:
            lessons_by_group[lesson.group].append(lesson)

        for group, lessons in lessons_by_group.items():
            if not lessons:
                continue
            msg = await self._notification_renderer.render(
                group=group,
                created_lessons=lessons,
            )
            await self._notification_sender.send(group_id=group.id, message=msg)
