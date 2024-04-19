from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic import BaseModel

TModel = TypeVar("TModel")
TId = TypeVar("TId")


class PaginatedResponse(BaseModel, Generic[TModel]):
    data: Sequence[TModel]
    current_page: int
    total_count: int

    @classmethod
    def empty(cls, current_page: int) -> "PaginatedResponse[TModel]":
        return PaginatedResponse(
            data=[],
            current_page=current_page,
            total_count=0,
        )
