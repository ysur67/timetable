from core.impls.alchemy import tables
from core.models.classroom import Classroom
from core.models.educational_level import EducationalLevel
from core.models.group import Group
from core.models.lesson import Lesson
from core.models.subject import Subject
from core.models.teacher import Teacher
from core.models.user import User


class DomainToAlchemyMapper:
    def map_classroom(self, domain: Classroom) -> tables.Classroom:
        return tables.Classroom(title=domain.title)

    def map_group(self, domain: Group) -> tables.Group:
        return tables.Group(title=domain.title, level_id=domain.level.id)

    def map_subject(self, domain: Subject) -> tables.Subject:
        return tables.Subject(title=domain.title)

    def map_teacher(self, domain: Teacher) -> tables.Teacher:
        return tables.Teacher(name=domain.name)

    def map_educational_level(
        self,
        domain: EducationalLevel,
    ) -> tables.EducationalLevel:
        return tables.EducationalLevel(title=domain.title, code=domain.code)

    def map_user(self, domain: User) -> tables.User:
        return tables.User(
            telegram_id=domain.telegram_id,
            preferences=self._map_user_preferences(domain),
        )

    def _map_user_preferences(self, domain: User) -> tables.UserPreferences:
        prefs = domain.preferences
        result = tables.UserPreferences(
            user_id=domain.id,
            report_days_offset=prefs.report_days_offset,
        )
        if prefs.selected_group is not None:
            result.selected_group_id = str(prefs.selected_group.id)
            result.selected_group = self.map_group(prefs.selected_group)
        return result

    def map_lesson(self, domain: Lesson) -> tables.Lesson:
        result = tables.Lesson(
            date_=domain.date_,
            time_start=domain.time_start,
            time_end=domain.time_end,
            group_id=domain.group.id,
            link=domain.link,
            note=domain.note,
            hash_=domain.get_hash(),
        )
        if domain.teacher is not None:
            result.teacher_id = str(domain.teacher.id)
        if domain.subject is not None:
            result.subject_id = str(domain.subject.id)
        if domain.classroom is not None:
            result.classroom_id = str(domain.classroom.id)

        return result
