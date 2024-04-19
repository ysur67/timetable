import httpx
import pytest
from litestar import status_codes

from adapters.litestar.routers.group.responses import GroupResponse
from adapters.litestar.schemas import PaginatedResponse


@pytest.mark.usefixtures("group")
async def test_returns_valid_schema(api_client: httpx.AsyncClient) -> None:
    response = await api_client.get("groups")
    assert response.status_code == status_codes.HTTP_200_OK
    PaginatedResponse[GroupResponse].model_validate(response.json())
