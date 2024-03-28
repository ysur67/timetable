from typing import Generic, Protocol

from pydantic import BaseModel

from core.types import TId, TModel


class Never(Exception):  # noqa: N818
    ...


class CoreError(Protocol): ...


class EntityNotFoundError(BaseModel, Generic[TModel, TId]):
    model: type[TModel]
    id: TId
