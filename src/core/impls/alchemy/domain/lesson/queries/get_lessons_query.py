from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import models
from core.domain.lesson.queries.get_lessons_query import GetLessonsQuery, LessonsFilter
from core.dtos import PaginationDto
from core.impls.alchemy.mappers.alchemy_to_domain_mapper import AlchemyToDomainMapper
from core.impls.alchemy.tables import Lesson
from core.types import Paginated


class AlchemyGetLessonsQuery(GetLessonsQuery):

    def __init__(self, session: AsyncSession, to_domain_mapper: AlchemyToDomainMapper) -> None:
        self._session = session
        self._to_domain_mapper = to_domain_mapper

    async def execute(self, filter_: LessonsFilter, pagination: PaginationDto) -> Paginated[models.Lesson]:
        stmt = select(Lesson, func.count(Lesson.id).over().label("total_count")).options(
            joinedload(Lesson.group),
            joinedload(Lesson.subject),
            joinedload(Lesson.teacher),
            joinedload(Lesson.classroom),
        )
        if filter_.date_start is not None:
            stmt = stmt.where(Lesson.date_ >= filter_.date_start)
        if filter_.date_end is not None:
            stmt = stmt.where(Lesson.date_ <= filter_.date_end)
        if filter_.group_id is not None:
            stmt = stmt.where(Lesson.group_id == filter_.group_id)
        stmt = stmt.limit(pagination.page_size).offset(pagination.get_offset())
        stmt = stmt.order_by(Lesson.date_.asc())
        result = await self._session.execute(stmt)
        rows = result.tuples().all()
        if len(rows) == 0:
            return Paginated.empty(pagination.page_size)
        _, total_count = rows[0]
        lessons = [self._to_domain_mapper.map_lesson(lesson) for (lesson, _) in rows]
        return Paginated(data=lessons, current_page=pagination.page, total_count=total_count)
