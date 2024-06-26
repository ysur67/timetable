from collections.abc import Iterable
from typing import Any

import aioinject

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.domain.lesson.repository import LessonRepository
from core.domain.subject.repositories import SubjectRepository
from core.domain.teacher.repositories import TeacherRepository
from core.domain.user.repositories import UserRepository
from core.impls.neo.domain.classroom.repositories import NeoClassroomRepository
from core.impls.neo.domain.educational_level.repositories import (
    NeoEducationalLevelRepository,
)
from core.impls.neo.domain.group.repositories import NeoGroupRepository
from core.impls.neo.domain.lesson.queries.lessons_report import NeoLessonsReportQuery
from core.impls.neo.domain.lesson.repository import NeoLessonRepository
from core.impls.neo.domain.subject.repositories import NeoSubjectRepository
from core.impls.neo.domain.teacher.repositories import NeoTeacherRepository
from core.impls.neo.domain.user.repositories import NeoUserRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Scoped(NeoRecordToDomainMapper),
    aioinject.Scoped(NeoEducationalLevelRepository, EducationalLevelRepository),
    aioinject.Scoped(NeoGroupRepository, GroupRepository),
    aioinject.Scoped(NeoTeacherRepository, TeacherRepository),
    aioinject.Scoped(NeoSubjectRepository, SubjectRepository),
    aioinject.Scoped(NeoClassroomRepository, ClassroomRepository),
    aioinject.Scoped(NeoLessonRepository, LessonRepository),
    aioinject.Scoped(NeoUserRepository, UserRepository),
    aioinject.Scoped(NeoLessonsReportQuery, LessonsReportQuery),
]
