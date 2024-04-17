from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from core.impls.alchemy.base import Base, uuid_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables import Lesson


ClassroomUniqueTitleConstraint = UniqueConstraint("title", name="classroom_title_constraint_unique")


class Classroom(Base):
    __tablename__ = "classroom"
    __table_args__ = (ClassroomUniqueTitleConstraint,)

    id: Mapped[uuid_pk]
    title: Mapped[str]

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="classroom")
