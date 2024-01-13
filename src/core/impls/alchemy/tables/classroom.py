from sqlalchemy.orm import Mapped

from core.impls.alchemy.base import Base, uuid_str_pk


class Classroom(Base):
    __tablename__ = "classroom"

    id: Mapped[uuid_str_pk]
    title: Mapped[str]
