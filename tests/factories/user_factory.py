import uuid

import factory

from core.models import User, UserPreferences
from tests.factories.base import GenericFactory


class UserFactory(GenericFactory[User]):
    id = factory.LazyFunction(uuid.uuid4)
    telegram_id = factory.Faker("pyint")
    preferences = factory.LazyAttribute(lambda _: UserPreferences.empty())
