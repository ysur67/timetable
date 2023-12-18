from typing import TypeVar

from core.models.base import Model

TModel = TypeVar("TModel", bound=Model)
TId = TypeVar("TId")
