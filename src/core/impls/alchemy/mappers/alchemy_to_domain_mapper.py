import uuid

from core.impls.alchemy import tables
from core.models.classroom import Classroom
from core.models.educational_level import EducationalLevel
from core.models.group import Group, GroupExternalId, GroupId
from core.models.lesson import Lesson
from core.models.subject import Subject
from core.models.teacher import Teacher
from core.models.user import User


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

    def map_subject(self, table: tables.Subject) -> Subject:
        return Subject.model_validate(table)

    def map_teacher(self, table: tables.Teacher) -> Teacher:
        return Teacher.model_validate(table)

    def map_educational_level(self, table: tables.EducationalLevel) -> EducationalLevel:
        return EducationalLevel.model_validate(table)

    def map_user(self, table: tables.User) -> User:
        return User.model_validate(table)

    def map_lesson(self, table: tables.Lesson) -> Lesson:
        return Lesson.model_validate(table)
