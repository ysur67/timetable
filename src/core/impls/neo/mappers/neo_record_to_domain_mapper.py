from typing import Any

from core.models import (
    Classroom,
    EducationalLevel,
    Group,
    Lesson,
    Subject,
    Teacher,
    User,
)
from core.models.user import UserPreferences


class NeoRecordToDomainMapper:
    def map_user(self, record: dict[str, Any]) -> User:
        data: dict[str, Any] = record["user"]
        preferences = UserPreferences.empty()
        if record.get("group") is not None:
            preferences = UserPreferences(selected_group=self.map_group(record))
        return User(
            id=data["id"],
            telegram_id=data["telegram_id"],
            preferences=preferences,
        )

    def map_group(self, record: dict[str, Any]) -> Group:
        data: dict[str, Any] = record["group"]
        return Group(
            id=data["id"],
            title=data["title"],
            external_id=data["code"],
            level=self.map_educational_level(record),
        )

    def map_educational_level(self, record: dict[str, Any]) -> EducationalLevel:
        data: dict[str, Any] = record["educational_level"]
        return EducationalLevel(
            id=data["id"],
            title=data["title"],
            code=data["code"],
        )

    def map_classroom(self, record: dict[str, Any]) -> Classroom:
        data: dict[str, Any] = record["classroom"]
        return Classroom(
            id=data["id"],
            title=data["title"],
        )

    def map_teacher(self, record: dict[str, Any]) -> Teacher:
        data: dict[str, Any] = record["teacher"]
        return Teacher(id=data["id"], name=data["name"])

    def map_subject(self, record: dict[str, Any]) -> Subject:
        data: dict[str, Any] = record["subject"]
        return Subject(id=data["id"], title=data["title"])

    def map_lesson(self, record: dict[str, Any]) -> Lesson:
        teacher: Teacher | None = None
        if record.get("teacher") is not None:
            teacher = self.map_teacher(record)
        subject: Subject | None = None
        if record.get("subject") is not None:
            subject = self.map_subject(record)
        classroom: Classroom | None = None
        if record.get("classroom") is not None:
            classroom = self.map_classroom(record)
        data: dict[str, Any] = record["lesson"]
        return Lesson(
            id=data["id"],
            date_=data["date"],
            time_start=data["time_start"],
            time_end=data["time_end"],
            group=self.map_group(record),
            teacher=teacher,
            subject=subject,
            classroom=classroom,
            link=data["link"],
            note=data["note"],
        )
