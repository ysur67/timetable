import uuid

import factory

from core.models import Group
from tests.factories.base import GenericFactory


class GroupFactory(GenericFactory[Group]):
    id = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("pystr")
    external_id = factory.Faker("pystr")
