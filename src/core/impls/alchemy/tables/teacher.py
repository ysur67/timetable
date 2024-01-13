from sqlalchemy.orm import Mapped

from core.impls.alchemy.base import Base, uuid_str_pk


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[uuid_str_pk]
    name: Mapped[str]
