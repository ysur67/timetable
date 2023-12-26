import uuid

import factory

from core.models import Lesson
from tests.factories.base import GenericFactory


class LessonFactory(GenericFactory[Lesson]):
    id = factory.LazyFunction(uuid.uuid4)
    date_ = factory.Faker("date")
    time_start = factory.Faker("time")
    time_end = factory.Faker("time")
    link = factory.Faker("pystr")
    note = factory.Faker("pystr")
