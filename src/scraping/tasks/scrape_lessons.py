import asyncio
import uuid
from collections.abc import Callable, Sequence
from datetime import timedelta
from typing import Any

import aioinject
import httpx

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.repository import LessonRepository
from core.domain.subject.repositories import SubjectRepository
from core.domain.teacher.repositories import TeacherRepository
from core.models.classroom import Classroom, ClassroomId
from core.models.lesson import Lesson, LessonId
from core.models.subject import Subject, SubjectId
from core.models.teacher import Teacher, TeacherId
from lib.dates import paginate_date_range, utc_now
from lib.logger import get_default_logger
from scraping.clients.lessons.http_client import HttpLessonsClient
from scraping.clients.lessons.lessons_client import LessonsClient
from scraping.schemas.lesson import LessonSchema

LessonsClientFactory = Callable[[], LessonsClient]


class ScrapeLessonsTask:

    def __init__(
        self,
        educational_level_repo: EducationalLevelRepository,
        client_factory: LessonsClientFactory,
        process: "_ProcessLessonSchemas",
    ) -> None:
        self._level_repo = educational_level_repo
        self._client_factory = client_factory
        self._process = process
        self._logger = get_default_logger(self.__class__.__name__)

    async def scrape(self) -> None:
        levels = await self._level_repo.get_all()
        tasks = [
            self._client_factory().get_all(level, start_date=start, end_date=end)
            for level in levels
            for (start, end) in paginate_date_range(
                start=utc_now().date() - timedelta(days=1),
                end=utc_now().date() + timedelta(days=100),
                page_size=timedelta(days=25),
            )
        ]

        client_responses = await asyncio.gather(*tasks, return_exceptions=True)
        batched_schemas: list[Sequence[LessonSchema]] = []
        errors: list[BaseException] = []
        for el in client_responses:
            if isinstance(el, BaseException):
                errors.append(el)
            else:
                batched_schemas.append(el)
        if errors:
            for err in errors:
                self._logger.exception(err)
        for batch in batched_schemas:
            await self._process.process(batch)


class _ProcessLessonSchemas:
    def __init__(  # noqa: PLR0913
        self,
        educational_level_repository: EducationalLevelRepository,
        group_repository: GroupRepository,
        teacher_repository: TeacherRepository,
        subject_repository: SubjectRepository,
        classroom_repository: ClassroomRepository,
        lesson_repository: LessonRepository,
    ) -> None:
        self._educational_level_repo = educational_level_repository
        self._group_repository = group_repository
        self._teacher_repository = teacher_repository
        self._subject_repository = subject_repository
        self._classroom_repository = classroom_repository
        self._lesson_repository = lesson_repository
        self._logger = get_default_logger(self.__class__.__name__)

    async def process(self, schemas: Sequence[LessonSchema]) -> None:
        for schema in schemas:
            await self._scrape_lesson(schema)

    async def _scrape_lesson(self, schema: LessonSchema) -> Lesson | None:
        group = await self._group_repository.get_by_title(schema.group.title)
        if group is None:
            self._logger.error(
                "Couldn't find group by title %s. Skipping %s creation...",
                schema.group.title,
                Lesson.__name__,
            )
            return None
        self._logger.info("Processing %s", schema)
        classroom = await self._get_classroom(schema)
        subject = await self._get_subject(schema)
        teacher = await self._get_teacher(schema)
        lesson = Lesson(
            id=LessonId(uuid.uuid4()),
            date_=schema.date_,
            time_start=schema.starts_at,
            time_end=schema.ends_at,
            group=group,
            teacher=teacher,
            subject=subject,
            link=schema.href,
            classroom=classroom,
            note=schema.note,
        )
        lesson, _ = await self._lesson_repository.get_or_create(lesson)
        self._logger.info("Found %s with id %s", Lesson.__name__, lesson.id)
        return lesson

    async def _get_teacher(self, schema: LessonSchema) -> Teacher | None:
        if schema.teacher is None:
            return None
        result, _ = await self._teacher_repository.get_or_create(
            Teacher(
                id=TeacherId(uuid.uuid4()),
                name=schema.teacher.name,
            ),
        )
        self._logger.info("Got %s with id %s", Teacher.__name__, result.id)
        return result

    async def _get_subject(self, schema: LessonSchema) -> Subject | None:
        if schema.subject is None:
            return None
        result, _ = await self._subject_repository.get_or_create(
            Subject(
                id=SubjectId(uuid.uuid4()),
                title=schema.subject.title,
            ),
        )
        self._logger.info("Got %s with id %s", Subject.__name__, result.id)
        return result

    async def _get_classroom(self, schema: LessonSchema) -> Classroom | None:
        if schema.classroom is None:
            return None
        result, _ = await self._classroom_repository.get_or_create(
            Classroom(
                id=ClassroomId(uuid.uuid4()),
                title=schema.classroom.title,
            ),
        )
        self._logger.info("Got %s with id %s", Classroom.__name__, result.id)
        return result


def _lesson_client_factory() -> HttpLessonsClient:
    client = httpx.AsyncClient(timeout=100)
    return HttpLessonsClient(client)


providers: list[aioinject.Provider[Any]] = [
    aioinject.Scoped(_ProcessLessonSchemas),
    aioinject.Scoped(lambda: _lesson_client_factory, LessonsClientFactory),  # type: ignore[arg-type]
]
