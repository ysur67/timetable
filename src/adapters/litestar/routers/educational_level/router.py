from typing import Annotated

from aioinject import Inject
from aioinject.ext.litestar import inject
from litestar import get
from litestar.router import Router

from adapters.litestar.routers.educational_level.responses import (
    EducationalLevelResponse,
)
from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery


@get("/")
@inject
async def get_educational_levels(
    levels_query: Annotated[GetAllEducationalLevelsQuery, Inject],
) -> list[EducationalLevelResponse]:
    result = await levels_query.execute()
    return [EducationalLevelResponse(id=level.id, title=level.title, code=level.code) for level in result]


router = Router(path="/educational-levels/", route_handlers=[get_educational_levels])
