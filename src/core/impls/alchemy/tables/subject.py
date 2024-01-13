from sqlalchemy.orm import Mapped

from core.impls.alchemy.base import Base, uuid_str_pk


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[uuid_str_pk]
    title: Mapped[str]
