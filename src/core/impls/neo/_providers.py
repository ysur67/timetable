from collections.abc import Iterable
from typing import Any

import aioinject

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.query.lessons_report import LessonsReportQuery
from core.domain.lesson.repository import LessonRepository
from core.domain.subject.repositories import SubjectRepository
from core.domain.teacher.repositories import TeacherRepository
from core.domain.user.repositories import UserRepository
from core.impls.neo.domain.classroom.repositories import NeoClassroomRepository
from core.impls.neo.domain.educational_level.queries.get_all import (
    NeoGetAllEducationalLevelsQuery,
)
from core.impls.neo.domain.educational_level.repositories import (
    NeoEducationalLevelRepository,
)
from core.impls.neo.domain.group.queries.get_by_educational_level import (
    NeoGetGroupsByEducationalLevelQuery,
)
from core.impls.neo.domain.group.repositories import NeoGroupRepository
from core.impls.neo.domain.lesson.queries.lessons_report import NeoLessonsReportQuery
from core.impls.neo.domain.lesson.repository import NeoLessonRepository
from core.impls.neo.domain.subject.repositories import NeoSubjectRepository
from core.impls.neo.domain.teacher.repositories import NeoTeacherRepository
from core.impls.neo.domain.user.repositories import NeoUserRepository
from core.impls.neo.mappers.neo_record_to_domain_mapper import NeoRecordToDomainMapper

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Callable(NeoRecordToDomainMapper),
    aioinject.Callable(NeoEducationalLevelRepository, EducationalLevelRepository),
    aioinject.Callable(NeoGroupRepository, GroupRepository),
    aioinject.Callable(NeoTeacherRepository, TeacherRepository),
    aioinject.Callable(NeoSubjectRepository, SubjectRepository),
    aioinject.Callable(NeoClassroomRepository, ClassroomRepository),
    aioinject.Callable(NeoLessonRepository, LessonRepository),
    aioinject.Callable(NeoUserRepository, UserRepository),
    aioinject.Callable(NeoGetAllEducationalLevelsQuery, GetAllEducationalLevelsQuery),
    aioinject.Callable(
        NeoGetGroupsByEducationalLevelQuery,
        GetGroupsByEducationalLevelQuery,
    ),
    aioinject.Callable(NeoLessonsReportQuery, LessonsReportQuery),
]
