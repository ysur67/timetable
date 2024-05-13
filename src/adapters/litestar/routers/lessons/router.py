import uuid
from datetime import date
from typing import Annotated

from aioinject import Inject
from aioinject.ext.litestar import inject
from litestar import get
from litestar.params import Parameter
from litestar.router import Router

from adapters.litestar.routers.lessons.responses import LessonResponse
from adapters.litestar.schemas import PaginatedResponse
from core.domain.lesson.queries.get_lessons_query import GetLessonsQuery, LessonsFilter
from core.dtos import PaginationDto


@get("")
@inject
async def get_lessons(
    lessons_query: Annotated[GetLessonsQuery, Inject],
    group_id: uuid.UUID | None = None,
    date_start: date | None = None,
    date_end: date | None = None,
    page: Annotated[int, Parameter(gt=0)] = 1,
    page_size: Annotated[int, Parameter(gt=0)] = 1,
) -> PaginatedResponse[LessonResponse]:
    result = await lessons_query.execute(
        LessonsFilter(
            date_start=date_start,
            date_end=date_end,
            group_id=group_id,
        ),
        PaginationDto(
            page=page,
            page_size=page_size,
        ),
    )
    return PaginatedResponse(
        data=[
            LessonResponse(
                id=lesson.id,
                date_=lesson.date_,
                time_start=lesson.time_start,
                time_end=lesson.time_end,
                note=lesson.note,
                link=lesson.link,
            )
            for lesson in result.data
        ],
        current_page=result.current_page,
        total_count=result.total_count,
    )


router = Router("lessons", route_handlers=[get_lessons])
