import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated

from sqlalchemy import BigInteger, DateTime, Enum, Integer, MetaData, Numeric, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, registry

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)

uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(primary_key=True, default=uuid.uuid4),
]
uuid_str_pk = Annotated[
    str,
    mapped_column(
        String(length=32),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    ),
]
int32_pk = Annotated[
    int,
    mapped_column(
        Integer,
        primary_key=True,
    ),
]
int64_pk = Annotated[
    int,
    mapped_column(
        BigInteger,
        primary_key=True,
    ),
]
numeric_10_2 = Annotated[Decimal, mapped_column(Numeric(precision=10, scale=2))]
numeric_10_3 = Annotated[Decimal, mapped_column(Numeric(precision=10, scale=3))]
numeric_22_2 = Annotated[Decimal, mapped_column(Numeric(precision=22, scale=2))]
numeric_3_1 = Annotated[Decimal, mapped_column(Numeric(precision=3, scale=2))]

str_3 = Annotated[str, 3]
str_10 = Annotated[str, 10]
str_16 = Annotated[str, 16]
str_32 = Annotated[str, 32]
str_60 = Annotated[str, 60]
str_64 = Annotated[str, 64]
str_128 = Annotated[str, 128]
str_255 = Annotated[str, 255]
str_500 = Annotated[str, 500]

int64 = Annotated[int, mapped_column(BigInteger)]
uuid_str = Annotated[str, mapped_column(String(32))]


class Base(DeclarativeBase):
    metadata = meta

    registry = registry(
        type_annotation_map={
            datetime: DateTime(timezone=True),
            str_3: String(3),
            str_10: String(10),
            str_16: String(16),
            str_32: String(32),
            str_60: String(60),
            str_64: String(64),
            str_128: String(128),
            str_255: String(255),
            str_500: String(500),
            enum.Enum: Enum(native_enum=False),
        },
    )
