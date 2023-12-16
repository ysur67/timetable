import uuid

from asyncpg import SchemaAndDataStatementMixingNotSupportedError

from core.domain.classroom.services import ClassroomService
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.subject.services import SubjectService
from core.domain.teacher.services import TeacherService
from core.models.classroom import Classroom, ClassroomId
from core.models.lesson import Lesson, LessonId
from core.models.subject import Subject, SubjectId
from core.models.teacher import Teacher, TeacherId
from lib.logger import get_default_logger
from scraping.clients.lessons_client import LessonsClient


class LessonsScraper:
    def __init__(  # noqa: PLR0913
        self,
        lessons_client: LessonsClient,
        educational_level_repository: EducationalLevelRepository,
        group_repository: GroupRepository,
        teacher_service: TeacherService,
        subject_service: SubjectService,
        classroom_service: ClassroomService,
    ) -> None:
        self._client = lessons_client
        self._educational_level_repo = educational_level_repository
        self._group_repository = group_repository
        self._teacher_service = teacher_service
        self._subject_service = subject_service
        self._classroom_service = classroom_service
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
                classroom: Classroom | None = None
                if schema.classroom is not None:
                    classroom = await self._classroom_service.get_or_create(
                        Classroom(
                            id=ClassroomId(uuid.uuid4()),
                            title=schema.classroom.title,
                        ),
                    )
                subject: Subject | None = None
                if schema.subject is not None:
                    subject = await self._subject_service.get_or_create(
                        Subject(
                            id=SubjectId(uuid.uuid4()),
                            title=schema.subject.title,
                        ),
                    )
                if schema.teacher is not None:
                    teacher = await self._teacher_service.get_or_create(
                        Teacher(
                            id=TeacherId(uuid.uuid4()),
                            name=schema.teacher.name,
                        ),
                    )
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
                )
