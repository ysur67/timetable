from sqlalchemy.orm import Mapped

from core.impls.alchemy.base import Base, uuid_str_pk


class EducationalLevel(Base):
    __tablename__ = "educational_level"

    id: Mapped[uuid_str_pk]
    title: Mapped[str]
    code: Mapped[str]
