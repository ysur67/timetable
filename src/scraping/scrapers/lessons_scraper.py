import uuid

from core.domain.classroom.services import ClassroomService
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.services import LessonService
from core.domain.subject.services import SubjectService
from core.domain.teacher.services import TeacherService
from core.models import (
    Classroom,
    ClassroomId,
    Lesson,
    LessonId,
    Model,
    Subject,
    SubjectId,
    Teacher,
    TeacherId,
)
from lib.logger import get_default_logger
from scraping.clients.lessons.lessons_client import LessonsClient
from scraping.schemas.lesson import LessonSchema


class LessonsScraper:
    def __init__(  # noqa: PLR0913
        self,
        lessons_client: LessonsClient,
        educational_level_repository: EducationalLevelRepository,
        group_repository: GroupRepository,
        teacher_service: TeacherService,
        subject_service: SubjectService,
        classroom_service: ClassroomService,
        lesson_service: LessonService,
    ) -> None:
        self._client = lessons_client
        self._educational_level_repo = educational_level_repository
        self._group_repository = group_repository
        self._teacher_service = teacher_service
        self._subject_service = subject_service
        self._classroom_service = classroom_service
        self._lesson_service = lesson_service
        self._logger = get_default_logger(self.__class__.__name__)

    async def scrape(self) -> None:
        for level in await self._educational_level_repo.get_all():
            lessons = await self._client.get_all(level)
            for schema in lessons:
                group = await self._group_repository.get_by_title(schema.group.title)
                if group is None:
                    self._logger.error(
                        "Couldn't find group by title %s. Skipping %s creation...",
                        schema.group.title,
                        Lesson.__name__,
                    )
                    continue
                self._logger.info("Processing %s", schema)
                classroom = await self._get_classroom(schema)
                self._log_object(Classroom, classroom)
                subject = await self._get_subject(schema)
                self._log_object(Subject, subject)
                teacher = await self._get_teacher(schema)
                self._log_object(Teacher, classroom)
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
                self._logger.info("Creating %s", lesson)
                await self._lesson_service.get_or_create(lesson)

    async def _get_teacher(self, schema: LessonSchema) -> Teacher | None:
        if schema.teacher is None:
            return None
        return await self._teacher_service.get_or_create(
            Teacher(
                id=TeacherId(uuid.uuid4()),
                name=schema.teacher.name,
            ),
        )

    async def _get_subject(self, schema: LessonSchema) -> Subject | None:
        if schema.subject is None:
            return None
        return await self._subject_service.get_or_create(
            Subject(
                id=SubjectId(uuid.uuid4()),
                title=schema.subject.title,
            ),
        )

    async def _get_classroom(self, schema: LessonSchema) -> Classroom | None:
        if schema.classroom is None:
            return None
        return await self._classroom_service.get_or_create(
            Classroom(
                id=ClassroomId(uuid.uuid4()),
                title=schema.classroom.title,
            ),
        )

    def _log_object(
        self,
        klass: type[Model],
        model: Model | None = None,
    ) -> None:
        if model is None:
            self._logger.info("Couldn't find %s", klass.__name__)
            return
        self._logger.info(
            "Found %s %s",
            klass.__name__,
            model,
        )
