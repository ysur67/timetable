import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.impls.alchemy.base import Base, uuid_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables import EducationalLevel, Lesson, UserPreferences


class Group(Base):
    __tablename__ = "group"

    id: Mapped[uuid_pk]
    title: Mapped[str]
    level_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("educational_level.id"))
    code: Mapped[str]

    level: Mapped["EducationalLevel"] = relationship(back_populates="groups")
    user_preferences: Mapped[list["UserPreferences"]] = relationship(
        back_populates="selected_group",
    )
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="group")
