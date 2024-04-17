from collections.abc import Iterable
from typing import Any

import aioinject

from core.domain.classroom.repositories import ClassroomRepository
from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.domain.group.queries.get_groups_by_title import SearchGroupsByTitleQuery
from core.domain.group.repositories import GroupRepository
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.domain.lesson.repository import LessonRepository
from core.domain.subject.repositories import SubjectRepository
from core.domain.teacher.repositories import TeacherRepository
from core.domain.user.repositories import UserRepository
from core.impls.alchemy.domain.classroom.repository import AlchemyClassroomRepository
from core.impls.alchemy.domain.educational_level.queries.get_all import (
    AlchemyGetAllEducationalLevelsQuery,
)
from core.impls.alchemy.domain.educational_level.repository import (
    AlchemyEducationalLevelRepository,
)
from core.impls.alchemy.domain.group.queries.get_by_educational_level import (
    AlchemyGetGroupsByEducationalLevelQuery,
)
from core.impls.alchemy.domain.group.queries.get_groups_by_title import (
    AlchemySearchGroupsByTitleQuery,
)
from core.impls.alchemy.domain.group.repository import AlchemyGroupRepository
from core.impls.alchemy.domain.lesson.queries.lessons_report import (
    AlchemyLessonsReportQuery,
)
from core.impls.alchemy.domain.lesson.repository import AlchemyLessonRepository
from core.impls.alchemy.domain.subject.repository import AlchemySubjectRepository
from core.impls.alchemy.domain.teacher.repository import AlchemyTeacherRepository
from core.impls.alchemy.domain.user.repository import AlchemyUserRepository
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.mappers.domain_to_alchemy_mapper import DomainToAlchemyMapper

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Singleton(AlchemyToDomainMapper),
    aioinject.Singleton(DomainToAlchemyMapper),
    aioinject.Scoped(AlchemyEducationalLevelRepository, EducationalLevelRepository),
    aioinject.Scoped(AlchemyGroupRepository, GroupRepository),
    aioinject.Scoped(AlchemyTeacherRepository, TeacherRepository),
    aioinject.Scoped(AlchemySubjectRepository, SubjectRepository),
    aioinject.Scoped(AlchemyClassroomRepository, ClassroomRepository),
    aioinject.Scoped(AlchemyLessonRepository, LessonRepository),
    aioinject.Scoped(AlchemyUserRepository, UserRepository),
    aioinject.Scoped(AlchemyGetGroupsByEducationalLevelQuery, GetGroupsByEducationalLevelQuery),
    aioinject.Scoped(AlchemyLessonsReportQuery, LessonsReportQuery),
    aioinject.Scoped(AlchemyGetAllEducationalLevelsQuery, GetAllEducationalLevelsQuery),
    aioinject.Scoped(AlchemySearchGroupsByTitleQuery, SearchGroupsByTitleQuery),
]
