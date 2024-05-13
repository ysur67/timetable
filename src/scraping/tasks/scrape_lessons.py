import asyncio
import uuid
from collections.abc import Callable, Sequence
from datetime import timedelta
from typing import Any

import aioinject
import httpx
from pydantic import BaseModel
from result import Err, Ok, Result

from core.domain.classroom.repositories import (
    ClassroomRepository,
    GetOrCreateClassroomParams,
)
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.repository import GetOrCreateLessonParams, LessonRepository
from core.domain.notifications.commands.send_lessons_created_notification import (
    SendLessonsCreatedNotificationCommand,
)
from core.domain.subject.repositories import GetOrCreateSubjectParams, SubjectRepository
from core.domain.teacher.repositories import GetOrCreateTeacherParams, TeacherRepository
from core.models.classroom import Classroom
from core.models.lesson import Lesson
from core.models.subject import Subject, SubjectId
from core.models.teacher import Teacher
from lib.dates import paginate_date_range, utc_now
from lib.logger import get_default_logger
from scraping.clients.lessons.http_client import HttpLessonsClient
from scraping.clients.lessons.lessons_client import LessonsClient
from scraping.schemas.lesson import LessonSchema

LessonsClientFactory = Callable[[], LessonsClient]


class MissingGroupError(BaseModel):
    title: str


class _ProcessLessonSchemasResult(BaseModel):
    created_lessons: list[Lesson]


class ScrapeLessonsTask:

    def __init__(
        self,
        educational_level_repo: EducationalLevelRepository,
        client_factory: LessonsClientFactory,
        send_notifications_command: SendLessonsCreatedNotificationCommand,
        process: "_ProcessLessonSchemas",
    ) -> None:
        self._level_repo = educational_level_repo
        self._client_factory = client_factory
        self._send_notifications_command = send_notifications_command
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
        for response in client_responses:
            if isinstance(response, BaseException):
                errors.append(response)
            else:
                batched_schemas.append(response)
        if errors:
            for err in errors:
                self._logger.exception(err)

        created_lessons = [
            lesson for batch in batched_schemas for lesson in (await self._process.process(batch)).created_lessons
        ]
        if len(created_lessons) > 0:
            await self._send_notifications_command.execute(created_lessons)


class _ProcessLessonSchemas:
    def __init__(
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

    async def process(self, schemas: Sequence[LessonSchema]) -> _ProcessLessonSchemasResult:
        created_lessons: list[Lesson] = []
        for schema in schemas:
            scrape_result = await self._scrape_lesson(schema)
            if isinstance(scrape_result, Err):
                self._logger.error(
                    "Couldn't find group by title %s. Skipping %s creation...",
                    schema.group.title,
                    Lesson.__name__,
                )
                continue
            lesson, is_created = scrape_result.ok()
            if is_created is True:
                created_lessons.append(lesson)
        return _ProcessLessonSchemasResult(created_lessons=created_lessons)

    async def _scrape_lesson(self, schema: LessonSchema) -> Result[tuple[Lesson, bool], MissingGroupError]:
        group = await self._group_repository.get_by_title(schema.group.title)
        if group is None:
            return Err(MissingGroupError(title=schema.group.title))
        self._logger.info("Processing %s", schema)
        classroom = await self._get_classroom(schema)
        subject = await self._get_subject(schema)
        teacher = await self._get_teacher(schema)
        params = GetOrCreateLessonParams(
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
        lesson, is_created = await self._lesson_repository.get_or_create(params)
        self._logger.info("Found %s with id %s", Lesson.__name__, lesson.id)
        return Ok((lesson, is_created))

    async def _get_teacher(self, schema: LessonSchema) -> Teacher | None:
        if schema.teacher is None:
            return None
        result, _ = await self._teacher_repository.get_or_create(
            GetOrCreateTeacherParams(name=schema.teacher.name),
        )
        self._logger.info("Got %s with id %s", Teacher.__name__, result.id)
        return result

    async def _get_subject(self, schema: LessonSchema) -> Subject | None:
        if schema.subject is None:
            return None
        result, _ = await self._subject_repository.get_or_create(
            GetOrCreateSubjectParams(
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
            GetOrCreateClassroomParams(title=schema.classroom.title),
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
