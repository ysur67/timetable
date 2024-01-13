from sqlalchemy.orm import Mapped

from core.impls.alchemy.base import Base, int64_pk


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int64_pk]
    title: Mapped[str]
