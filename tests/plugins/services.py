import pytest

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.classroom.services import ClassroomService
from core.domain.lesson.repository import LessonRepository
from core.domain.lesson.services import LessonService
from core.domain.subject.repositories import SubjectRepository
from core.domain.subject.services import SubjectService
from core.domain.teacher.repositories import TeacherRepository
from core.domain.teacher.services import TeacherService
from core.impls.neo.domain.classroom.services import NeoClassroomService
from core.impls.neo.domain.lesson.services import NeoLessonService
from core.impls.neo.domain.subject.services import NeoSubjectService
from core.impls.neo.domain.teacher.services import NeoTeacherService


@pytest.fixture()
def teacher_service(teacher_repository: TeacherRepository) -> TeacherService:
    return NeoTeacherService(teacher_repository)


@pytest.fixture()
def subject_service(subject_repository: SubjectRepository) -> SubjectService:
    return NeoSubjectService(subject_repository)


@pytest.fixture()
def classroom_service(classroom_repository: ClassroomRepository) -> ClassroomService:
    return NeoClassroomService(classroom_repository)


@pytest.fixture()
def lesson_service(lesson_repository: LessonRepository) -> LessonService:
    return NeoLessonService(lesson_repository)
