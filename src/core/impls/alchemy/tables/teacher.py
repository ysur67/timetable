from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.impls.alchemy.base import Base, uuid_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables import Lesson


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[uuid_pk]
    name: Mapped[str]

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="teacher")
