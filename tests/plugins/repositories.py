import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.repository import LessonRepository
from core.domain.subject.repositories import SubjectRepository
from core.domain.teacher.repositories import TeacherRepository
from core.domain.user.repositories import UserRepository
from core.impls.alchemy.domain.classroom.repository import AlchemyClassroomRepository
from core.impls.alchemy.domain.educational_level.repository import (
    AlchemyEducationalLevelRepository,
)
from core.impls.alchemy.domain.group.repository import AlchemyGroupRepository
from core.impls.alchemy.domain.lesson.repository import AlchemyLessonRepository
from core.impls.alchemy.domain.subject.repository import AlchemySubjectRepository
from core.impls.alchemy.domain.teacher.repository import AlchemyTeacherRepository
from core.impls.alchemy.domain.user.repository import AlchemyUserRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper


@pytest.fixture()
def group_repository(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
    domain_to_alchemy_mapper: DomainToAlchemyMapper,
) -> GroupRepository:
    return AlchemyGroupRepository(
        session,
        alchemy_to_domain_mapper,
        domain_to_alchemy_mapper,
    )


@pytest.fixture()
def educational_level_repository(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
    domain_to_alchemy_mapper: DomainToAlchemyMapper,
) -> EducationalLevelRepository:
    return AlchemyEducationalLevelRepository(
        session,
        alchemy_to_domain_mapper,
        domain_to_alchemy_mapper,
    )


@pytest.fixture()
def classroom_repository(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
    domain_to_alchemy_mapper: DomainToAlchemyMapper,
) -> ClassroomRepository:
    return AlchemyClassroomRepository(
        session,
        alchemy_to_domain_mapper,
        domain_to_alchemy_mapper,
    )


@pytest.fixture()
def subject_repository(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
    domain_to_alchemy_mapper: DomainToAlchemyMapper,
) -> SubjectRepository:
    return AlchemySubjectRepository(
        session,
        alchemy_to_domain_mapper,
        domain_to_alchemy_mapper,
    )


@pytest.fixture()
def teacher_repository(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
    domain_to_alchemy_mapper: DomainToAlchemyMapper,
) -> TeacherRepository:
    return AlchemyTeacherRepository(
        session,
        alchemy_to_domain_mapper,
        domain_to_alchemy_mapper,
    )


@pytest.fixture()
def lesson_repository(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
    domain_to_alchemy_mapper: DomainToAlchemyMapper,
) -> LessonRepository:
    return AlchemyLessonRepository(
        session,
        alchemy_to_domain_mapper,
        domain_to_alchemy_mapper,
    )


@pytest.fixture()
def user_repository(
    session: AsyncSession,
    alchemy_to_domain_mapper: AlchemyToDomainMapper,
    domain_to_alchemy_mapper: DomainToAlchemyMapper,
) -> UserRepository:
    return AlchemyUserRepository(
        session,
        alchemy_to_domain_mapper,
        domain_to_alchemy_mapper,
    )
