from sqlalchemy.orm import Mapped

from core.impls.alchemy.base import Base, int64_pk


class Classroom(Base):
    __tablename__ = "classroom"

    id: Mapped[int64_pk]
    title: Mapped[str]
