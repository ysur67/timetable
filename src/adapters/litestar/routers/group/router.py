import uuid
from typing import Annotated

from aioinject import Inject
from aioinject.ext.litestar import inject
from litestar import get
from litestar.params import Parameter
from litestar.router import Router

from adapters.litestar.routers.group.responses import GroupResponse
from adapters.litestar.schemas import PaginatedResponse
from core.domain.group.queries.get_groups_query import (
    GetGroupsQueryPaginated,
    GroupsFilter,
)
from core.dtos import PaginationDto


@get("/")
@inject
async def get_groups(
    groups_query: Annotated[GetGroupsQueryPaginated, Inject],
    page: Annotated[int, Parameter(gt=0)] = 1,
    page_size: Annotated[int, Parameter(gt=0)] = 1,
    educational_level_id: uuid.UUID | None = None,
    search_term: str | None = None,
) -> PaginatedResponse[GroupResponse]:
    result = await groups_query.execute(
        GroupsFilter(search_term=search_term, educational_level_id=educational_level_id),
        PaginationDto(page=page, page_size=page_size),
    )
    return PaginatedResponse(
        data=[
            GroupResponse(id=group.id, title=group.title, educational_level_id=group.level_id) for group in result.data
        ],
        current_page=result.current_page,
        total_count=result.total_count,
    )


router = Router("groups", route_handlers=[get_groups])
