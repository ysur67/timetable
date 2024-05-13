import uuid

from faker import Faker

from core.domain.subject.repositories import GetOrCreateSubjectParams, SubjectRepository
from tests.factories.subject_factory import TestSubjectFactory


async def test_creates_new_subject(subject_repository: SubjectRepository, faker: Faker) -> None:
    params = GetOrCreateSubjectParams(id=uuid.uuid4(), title=faker.name())
    result, is_created = await subject_repository.get_or_create(params)
    assert is_created is True
    assert result.id == params.id
    assert result.title == params.title


async def test_returns_extant_subject(
    subject_repository: SubjectRepository,
    subject_factory: TestSubjectFactory,
) -> None:
    subject = await subject_factory.create()
    params = GetOrCreateSubjectParams(id=uuid.uuid4(), title=subject.title)
    result, is_created = await subject_repository.get_or_create(params)
    assert is_created is False
    assert result.title == params.title
