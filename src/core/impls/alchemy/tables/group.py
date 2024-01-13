from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.impls.alchemy.base import Base, int64, int64_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables.educational_level import EducationalLevel
    from core.impls.alchemy.tables.user import User


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int64_pk]
    title: Mapped[str]
    level_id: Mapped[int64] = mapped_column(ForeignKey("educational_level.id"))

    level: Mapped["EducationalLevel"] = relationship(back_populates="groups")
    users: Mapped[list["User"]] = relationship(back_populates="selected_group")
