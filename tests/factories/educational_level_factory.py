import factory

from core.impls.alchemy.tables.educational_level import EducationalLevel
from tests.factories.base import GenericFactory


class EducationalLevelFactory(GenericFactory[EducationalLevel]):
    id = factory.Faker("uuid4")
    title = factory.Faker("pystr")
    code = factory.Faker("pystr")
