import factory

from core import models
from core.impls.alchemy.tables.user import User, UserPreferences
from tests.factories.base import GenericFactory


class UserFactory(GenericFactory[User]):
    id = factory.Faker("uuid4")
    telegram_id = factory.Faker("pyint")


class UserPreferencesFactory(GenericFactory[UserPreferences]):
    report_days_offset = factory.LazyFunction(
        lambda: models.UserPreferences.empty().report_days_offset,
    )
