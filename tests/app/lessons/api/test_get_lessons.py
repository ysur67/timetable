import httpx
from litestar import status_codes

from adapters.litestar.routers.lessons.responses import LessonResponse
from adapters.litestar.schemas import PaginatedResponse
from core.models.group import Group
from lib.dates import utc_now
from tests.factories.lessons_factory import TestLessonFactory


async def test_returns_valid_schema(
    api_client: httpx.AsyncClient,
    lesson_factory: TestLessonFactory,
    group: Group,
) -> None:
    _ = await lesson_factory.create_batch(10, group_id=group.id, date_=utc_now().date())
    response = await api_client.get("lessons")
    assert response.status_code == status_codes.HTTP_200_OK
    PaginatedResponse[LessonResponse].model_validate(response.json())
