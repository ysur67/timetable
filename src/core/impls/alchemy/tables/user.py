from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.impls.alchemy.base import Base, int64, int64_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables.group import Group


class User(Base):
    __tablename__ = "user"

    id: Mapped[int64_pk]
    telegram_id: Mapped[str]

    preferences: Mapped["UserPreferences"] = relationship(back_populates="user")


class UserPreferences(Base):
    __tablename__ = "user_preferences"
    __table_args__ = (UniqueConstraint("user_id"),)

    id: Mapped[int64_pk]
    selected_group_id: Mapped[int64] = mapped_column(ForeignKey("group.id"))
    report_days_offset: Mapped[int]
    user_id: Mapped[int64] = mapped_column(ForeignKey("user.id"))

    selected_group: Mapped["Group"] = relationship(back_populates="users")
    user: Mapped["User"] = relationship(back_populates="preferences")
