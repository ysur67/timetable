import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.impls.alchemy.base import Base, uuid_str, uuid_str_pk

if TYPE_CHECKING:
    from core.impls.alchemy.tables.classroom import Classroom
    from core.impls.alchemy.tables.group import Group
    from core.impls.alchemy.tables.subject import Subject
    from core.impls.alchemy.tables.teacher import Teacher


class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[uuid_str_pk]
    date_: Mapped[datetime.date]
    time_start: Mapped[datetime.time]
    time_end: Mapped[datetime.time]
    group_id: Mapped[uuid_str] = mapped_column(ForeignKey("group.id"))
    teacher_id: Mapped[uuid_str | None] = mapped_column(ForeignKey("teacher.id"))
    subject_id: Mapped[uuid_str | None] = mapped_column(ForeignKey("subject.id"))
    classroom_id: Mapped[uuid_str | None] = mapped_column(ForeignKey("classroom.id"))
    link: Mapped[str]
    note: Mapped[str]
    hash_: Mapped[str]

    group: Mapped["Group"] = relationship(back_populates="lessons")
    teacher: Mapped["Teacher | None"] = relationship(back_populates="teacher")
    subject: Mapped["Subject | None"] = relationship(back_populates="subject.id")
    classroom: Mapped["Classroom | None"] = relationship(back_populates="classroom.id")
