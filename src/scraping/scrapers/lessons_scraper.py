import uuid

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.repository import LessonRepository
from core.domain.notifications.commands.send_lessons_created_notification import (
    SendLessonsCreatedNotificationCommand,
)
from core.domain.subject.repositories import SubjectRepository
from core.domain.teacher.repositories import TeacherRepository
from core.models import (
    Classroom,
    ClassroomId,
    Lesson,
    LessonId,
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
        teacher_repository: TeacherRepository,
        subject_repository: SubjectRepository,
        classroom_repository: ClassroomRepository,
        lesson_repository: LessonRepository,
        send_notifications_command: SendLessonsCreatedNotificationCommand,
    ) -> None:
        self._client = lessons_client
        self._educational_level_repo = educational_level_repository
        self._group_repository = group_repository
        self._teacher_repository = teacher_repository
        self._subject_repository = subject_repository
        self._classroom_repository = classroom_repository
        self._lesson_repository = lesson_repository
        self._send_notifications_command = send_notifications_command
        self._logger = get_default_logger(self.__class__.__name__)

    async def scrape(self) -> None:
        created_lessons: list[Lesson] = []
        for level in await self._educational_level_repo.get_all():
            lessons = await self._client.get_all(level)
            for schema in lessons:
                result = await self._scrape_lesson(schema)
                if result is None:
                    continue
                lesson, is_created = result
                if not is_created:
                    continue
                created_lessons.append(lesson)
        if not created_lessons:
            return
        await self._send_notifications_command.execute(created_lessons)

    async def _scrape_lesson(self, schema: LessonSchema) -> tuple[Lesson, bool] | None:
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
        creation_result = await self._lesson_repository.get_or_create(lesson)
        self._logger.info("Found %s with id %s", Lesson.__name__, lesson.id)
        return creation_result

    async def _get_teacher(self, schema: LessonSchema) -> Teacher | None:
        if schema.teacher is None:
            return None
        result, is_created = await self._teacher_repository.get_or_create(
            Teacher(
                id=TeacherId(uuid.uuid4()),
                name=schema.teacher.name,
            ),
        )
        operation = "Created" if is_created else "Found"
        self._logger.info("%s %s with id %s", operation, Teacher.__name__, result.id)
        return result

    async def _get_subject(self, schema: LessonSchema) -> Subject | None:
        if schema.subject is None:
            return None
        result, is_created = await self._subject_repository.get_or_create(
            Subject(
                id=SubjectId(uuid.uuid4()),
                title=schema.subject.title,
            ),
        )
        operation = "Created" if is_created else "Found"
        self._logger.info("%s %s with id %s", operation, Subject.__name__, result.id)
        return result

    async def _get_classroom(self, schema: LessonSchema) -> Classroom | None:
        if schema.classroom is None:
            return None
        result, is_created = await self._classroom_repository.get_or_create(
            Classroom(
                id=ClassroomId(uuid.uuid4()),
                title=schema.classroom.title,
            ),
        )
        operation = "Created" if is_created else "Found"
        self._logger.info("%s %s with id %s", operation, Classroom.__name__, result.id)
        return result
