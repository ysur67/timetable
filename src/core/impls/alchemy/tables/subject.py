from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from core.impls.alchemy.base import Base, uuid_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables import Lesson


UniqueSubjectTitleConstraint = UniqueConstraint("title", name="subject_title_constraint_unique")


class Subject(Base):
    __tablename__ = "subject"
    __table_args__ = (UniqueSubjectTitleConstraint,)

    id: Mapped[uuid_pk]
    title: Mapped[str]

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="subject")
