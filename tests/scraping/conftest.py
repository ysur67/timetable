import pytest
from faker import Faker
from neo4j import AsyncSession

from core.domain.classroom.services import ClassroomService
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.services import LessonService
from core.domain.subject.services import SubjectService
from core.domain.teacher.services import TeacherService
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper
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
    mapper: NeoRecordToDomainMapper,
) -> DummyLessonsClient:
    return DummyLessonsClient(lessons_client_response_size, session, faker, mapper)


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
    teacher_service: TeacherService,
    subject_service: SubjectService,
    classroom_service: ClassroomService,
    lesson_service: LessonService,
) -> LessonsScraper:
    return LessonsScraper(
        lessons_client,
        educational_level_repository,
        group_repository,
        teacher_service,
        subject_service,
        classroom_service,
        lesson_service,
    )
