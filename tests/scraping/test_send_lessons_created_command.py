from core.domain.notifications.commands.send_lessons_created_notification import (
    SendLessonsCreatedNotificationCommand,
)
from core.domain.notifications.sender import (
    DummyLessonsCreatedNotificationSender,
)


async def test_skips_sending_if_sequence_is_empty(
    send_lessons_created_notification_command: SendLessonsCreatedNotificationCommand,
    lessons_created_notification_sender: DummyLessonsCreatedNotificationSender,
) -> None:
    command = send_lessons_created_notification_command
    sender = lessons_created_notification_sender
    await command.execute([])
    for key in sender.sent_messages:
        assert not sender.sent_messages[key]
