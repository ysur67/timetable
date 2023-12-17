import pytest
from neo4j import AsyncSession

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.repository import LessonRepository
from core.domain.subject.repositories import SubjectRepository
from core.domain.teacher.repositories import TeacherRepository
from core.impls.neo.domain.classroom.repositories import NeoClassroomRepository
from core.impls.neo.domain.educational_level.repositories import (
    NeoEducationalLevelRepository,
)
from core.impls.neo.domain.group.repositories import NeoGroupRepository
from core.impls.neo.domain.lesson.repository import NeoLessonRepository
from core.impls.neo.domain.subject.repositories import NeoSubjectRepository
from core.impls.neo.domain.teacher.repositories import NeoTeacherRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper


@pytest.fixture()
def mapper() -> NeoRecordToDomainMapper:
    return NeoRecordToDomainMapper()


@pytest.fixture()
def group_repository(
    session: AsyncSession,
    mapper: NeoRecordToDomainMapper,
) -> GroupRepository:
    return NeoGroupRepository(session, mapper)


@pytest.fixture()
def educational_level_repository(
    session: AsyncSession,
    mapper: NeoRecordToDomainMapper,
) -> EducationalLevelRepository:
    return NeoEducationalLevelRepository(session, mapper)


@pytest.fixture()
def classroom_repository(
    session: AsyncSession,
    mapper: NeoRecordToDomainMapper,
) -> ClassroomRepository:
    return NeoClassroomRepository(session, mapper)


@pytest.fixture()
def subject_repository(
    session: AsyncSession,
    mapper: NeoRecordToDomainMapper,
) -> SubjectRepository:
    return NeoSubjectRepository(session, mapper)


@pytest.fixture()
def teacher_repository(
    session: AsyncSession,
    mapper: NeoRecordToDomainMapper,
) -> TeacherRepository:
    return NeoTeacherRepository(session, mapper)


@pytest.fixture()
def lesson_repository(
    session: AsyncSession,
    mapper: NeoRecordToDomainMapper,
) -> LessonRepository:
    return NeoLessonRepository(session, mapper)
