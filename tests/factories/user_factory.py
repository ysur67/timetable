import uuid

import factory

from core import models
from core.impls.alchemy.tables.user import User, UserPreferences
from tests.factories.base import GenericFactory


class UserFactory(GenericFactory[User]):
    id = factory.LazyFunction(lambda: uuid.uuid4())
    telegram_id = factory.LazyFunction(lambda: str(uuid.uuid4()))


class UserPreferencesFactory(GenericFactory[UserPreferences]):
    report_days_offset = factory.LazyFunction(
        lambda: models.UserPreferences.empty().report_days_offset,
    )
