from sqlalchemy.orm import Mapped

from core.impls.alchemy.base import Base, int64_pk


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int64_pk]
    name: Mapped[str]
