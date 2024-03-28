from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.impls.alchemy.base import Base, uuid_str_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables import Group


class EducationalLevel(Base):
    __tablename__ = "educational_level"

    id: Mapped[uuid_str_pk]
    title: Mapped[str]
    code: Mapped[str]

    groups: Mapped[list["Group"]] = relationship(back_populates="level")
