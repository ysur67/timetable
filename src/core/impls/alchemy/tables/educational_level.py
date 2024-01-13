from sqlalchemy.orm import Mapped

from core.impls.alchemy.base import Base, int64_pk


class EducationalLevel(Base):
    __tablename__ = "educational_level"

    id: Mapped[int64_pk]
    title: Mapped[str]
    code: Mapped[str]
