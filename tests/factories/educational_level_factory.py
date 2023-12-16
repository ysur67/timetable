import uuid

import factory

from core.models.educational_level import EducationalLevel
from tests.factories.base import GenericFactory


class EducationalLevelFactory(GenericFactory[EducationalLevel]):
    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("pystr")
    code = factory.Faker("pystr")
