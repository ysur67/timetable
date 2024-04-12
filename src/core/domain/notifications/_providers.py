from collections.abc import Iterable
from typing import Any

import aioinject

from core.domain.notifications.commands.send_lessons_created_notification import (
    SendLessonsCreatedNotificationCommand,
)
from core.domain.notifications.renderer import (
    JinjaLessonsCreatedNotificationsRenderer,
    LessonsCreatedNotificationRenderer,
)
from core.domain.notifications.sender import (
    LessonsCreatedNotificationSender,
    TelegramLessonsCreatedNotificationSender,
)

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Scoped(
        JinjaLessonsCreatedNotificationsRenderer,
        LessonsCreatedNotificationRenderer,
    ),
    aioinject.Scoped(
        TelegramLessonsCreatedNotificationSender,
        LessonsCreatedNotificationSender,
    ),
    aioinject.Scoped(SendLessonsCreatedNotificationCommand),
]
