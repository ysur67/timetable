from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic import BaseModel

from core.models.base import Model

TModel = TypeVar("TModel", bound=Model)
TId = TypeVar("TId")


class Paginated(BaseModel, Generic[TModel]):
    data: Sequence[TModel]
    current_page: int
    total_count: int

    @classmethod
    def empty(cls, current_page: int) -> "Paginated[TModel]":
        return Paginated(
            data=[],
            current_page=current_page,
            total_count=0,
        )
