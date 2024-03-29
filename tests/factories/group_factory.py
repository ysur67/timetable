import uuid

import factory

from core.impls.alchemy.tables.group import Group
from tests.factories.base import GenericFactory


class GroupFactory(GenericFactory[Group]):
    id = factory.LazyFunction(lambda: uuid.uuid4())
    title = factory.Faker("pystr")
    code = factory.Faker("uuid4")
