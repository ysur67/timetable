import pytest

from core.domain.group.repositories import GroupRepository
from core.domain.notifications.commands.send_lessons_created_notification import (
    SendLessonsCreatedNotificationCommand,
)
from core.domain.notifications.renderer import (
    DummyLessonsCreatedNotificationsRenderer,
    LessonsCreatedNotificationRenderer,
)
from core.domain.notifications.sender import (
    DummyLessonsCreatedNotificationSender,
    LessonsCreatedNotificationSender,
)
from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand
from core.domain.user.commands.set_selected_group import SetSelectedGroupCommand
from core.domain.user.repositories import UserRepository


@pytest.fixture()
async def get_or_create_user_command(
    user_repository: UserRepository,
) -> GetOrCreateUserCommand:
    return GetOrCreateUserCommand(user_repository)


@pytest.fixture()
async def set_selected_group_command(
    user_repository: UserRepository,
    group_repository: GroupRepository,
) -> SetSelectedGroupCommand:
    return SetSelectedGroupCommand(user_repository, group_repository)


@pytest.fixture()
async def lessons_created_renderer() -> LessonsCreatedNotificationRenderer:
    return DummyLessonsCreatedNotificationsRenderer()


@pytest.fixture()
async def lessons_created_notification_sender() -> DummyLessonsCreatedNotificationSender:
    return DummyLessonsCreatedNotificationSender()


@pytest.fixture()
async def send_lessons_created_notification_command(
    lessons_created_renderer: LessonsCreatedNotificationRenderer,
    lessons_created_notification_sender: LessonsCreatedNotificationSender,
) -> SendLessonsCreatedNotificationCommand:
    return SendLessonsCreatedNotificationCommand(
        notification_renderer=lessons_created_renderer,
        notification_sender=lessons_created_notification_sender,
    )
