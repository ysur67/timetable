from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

import factory

T = TypeVar("T")


class GenericFactory(factory.Factory, Generic[T]):
    if TYPE_CHECKING:

        @classmethod
        def build(cls, **kwargs: Any) -> T:  # noqa: ANN401
            ...

        @classmethod
        def build_batch(cls, size: int, **kwargs: Any) -> list[T]:  # noqa: ANN401
            ...

    def __class_getitem__(cls, item: type[T] | TypeVar) -> GenericFactory[T]:
        if isinstance(item, TypeVar):
            return cls  # type: ignore[return-value]

        class Meta:
            model = item

        return type(  # type: ignore[return-value]
            f"{cls.__qualname__}[{item.__qualname__}]",
            (cls,),
            {
                "Meta": Meta,
            },
        )
