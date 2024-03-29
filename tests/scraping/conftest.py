import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.repository import LessonRepository
from core.domain.notifications.commands.send_lessons_created_notification import (
    SendLessonsCreatedNotificationCommand,
)
from core.domain.subject.repositories import SubjectRepository
from core.domain.teacher.repositories import TeacherRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from scraping.scrapers.groups_scraper import GroupsScraper
from scraping.scrapers.lessons_scraper import LessonsScraper
from tests.scraping.dummies.groups_client import DummyGroupsClient
from tests.scraping.dummies.lessons_client import DummyLessonsClient


@pytest.fixture()
def groups_client_response_size() -> int:
    return 10


@pytest.fixture()
def lessons_client_response_size() -> int:
    return 10


@pytest.fixture()
def groups_client(groups_client_response_size: int) -> DummyGroupsClient:
    return DummyGroupsClient(groups_client_response_size)


@pytest.fixture()
def lessons_client(
    lessons_client_response_size: int,
    session: AsyncSession,
    faker: Faker,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
) -> DummyLessonsClient:
    return DummyLessonsClient(
        lessons_client_response_size,
        session,
        faker,
        alchemy_to_domain_mapper,
    )


@pytest.fixture()
def groups_scraper(
    groups_client: DummyGroupsClient,
    educational_level_repository: EducationalLevelRepository,
    group_repository: GroupRepository,
) -> GroupsScraper:
    return GroupsScraper(
        groups_client,
        educational_level_repository,
        group_repository,
    )


@pytest.fixture()
def lessons_scraper(  # noqa: PLR0913
    lessons_client: DummyLessonsClient,
    educational_level_repository: EducationalLevelRepository,
    group_repository: GroupRepository,
    teacher_repository: TeacherRepository,
    subject_repository: SubjectRepository,
    classroom_repository: ClassroomRepository,
    lesson_repository: LessonRepository,
    send_lessons_created_notification_command: SendLessonsCreatedNotificationCommand,
) -> LessonsScraper:
    return LessonsScraper(
        lessons_client,
        educational_level_repository,
        group_repository,
        teacher_repository,
        subject_repository,
        classroom_repository,
        lesson_repository,
        send_lessons_created_notification_command,
    )
