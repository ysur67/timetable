import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from tests.factories.lessons_factory import TestLessonFactory
from tests.factories.subject_factory import TestSubjectFactory


@pytest.fixture()
def lesson_factory(session: AsyncSession, alchemy_to_domain_mapper: AlchemyToDomainMapper) -> TestLessonFactory:
    return TestLessonFactory(session, alchemy_to_domain_mapper)


@pytest.fixture()
def subject_factory(session: AsyncSession, alchemy_to_domain_mapper: AlchemyToDomainMapper) -> TestSubjectFactory:
    return TestSubjectFactory(session, alchemy_to_domain_mapper)
