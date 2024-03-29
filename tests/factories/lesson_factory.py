import uuid
from datetime import UTC, date, datetime

import factory
from factory.fuzzy import FuzzyDate, FuzzyDateTime

from core.impls.alchemy.tables.lesson import Lesson
from tests.factories.base import GenericFactory


class LessonFactory(GenericFactory[Lesson]):
    id = factory.LazyFunction(lambda: uuid.uuid4())
    date_ = FuzzyDate(start_date=date.min)
    time_start = factory.LazyAttribute(
        lambda _: FuzzyDateTime(start_dt=datetime(1970, 1, 1, tzinfo=UTC))
        .fuzz()
        .time(),
    )
    time_end = factory.LazyAttribute(
        lambda _: FuzzyDateTime(start_dt=datetime(1970, 1, 1, tzinfo=UTC))
        .fuzz()
        .time(),
    )
    link = factory.Faker("pystr")
    note = factory.Faker("pystr")
    hash_ = factory.Faker("uuid4")
