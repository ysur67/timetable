import uuid

from core.impls.alchemy import tables
from core.models.classroom import Classroom
from core.models.educational_level import EducationalLevel
from core.models.group import Group, GroupExternalId, GroupId, SimpleGroup
from core.models.lesson import Lesson, LessonId
from core.models.subject import Subject
from core.models.teacher import Teacher
from core.models.user import User, UserId, UserPreferences, UserTelegramId


class AlchemyToDomainMapper:
    def map_classroom(self, table: tables.Classroom) -> Classroom:
        return Classroom.model_validate(table)

    def map_group(self, table: tables.Group) -> Group:
        return Group(
            id=GroupId(uuid.UUID(table.id)),
            external_id=GroupExternalId(table.code),
            title=table.title,
            level=self.map_educational_level(table.level),
        )

    def map_simple_group(self, table: tables.Group) -> SimpleGroup:
        return SimpleGroup(
            id=GroupId(uuid.UUID(table.id)),
            external_id=GroupExternalId(table.code),
            title=table.title,
        )

    def map_subject(self, table: tables.Subject) -> Subject:
        return Subject.model_validate(table)

    def map_teacher(self, table: tables.Teacher) -> Teacher:
        return Teacher.model_validate(table)

    def map_educational_level(self, table: tables.EducationalLevel) -> EducationalLevel:
        return EducationalLevel.model_validate(table)

    def map_user(self, table: tables.User) -> User:
        return User(
            id=UserId(uuid.UUID(table.id)),
            telegram_id=UserTelegramId(int(table.telegram_id)),
            preferences=self._map_user_preferences(table),
        )

    def _map_user_preferences(self, table: tables.User) -> UserPreferences:
        prefs = table.preferences
        selected_group: Group | None = None
        if prefs.selected_group is not None:
            selected_group = self.map_group(prefs.selected_group)
        return UserPreferences(
            report_days_offset=table.preferences.report_days_offset,
            selected_group=selected_group,
        )

    def map_lesson(self, table: tables.Lesson) -> Lesson:
        group = self.map_simple_group(table.group)
        classroom: Classroom | None = None
        if table.classroom is not None:
            classroom = self.map_classroom(table.classroom)
        subject: Subject | None = None
        if table.subject is not None:
            subject = self.map_subject(table.subject)
        teacher: Teacher | None = None
        if table.teacher is not None:
            teacher = self.map_teacher(table.teacher)
        return Lesson(
            id=LessonId(uuid.UUID(table.id)),
            date_=table.date_,
            time_start=table.time_start,
            time_end=table.time_end,
            teacher=teacher,
            classroom=classroom,
            group=group,
            subject=subject,
            link=table.link,
            note=table.note,
        )
