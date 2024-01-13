from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.impls.alchemy.base import Base, uuid_str_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables import Lesson


class Classroom(Base):
    __tablename__ = "classroom"

    id: Mapped[uuid_str_pk]
    title: Mapped[str]

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="classroom")
