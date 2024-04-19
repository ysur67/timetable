import httpx
import pytest
from litestar import status_codes

from adapters.litestar.routers.educational_level.responses import (
    EducationalLevelResponse,
)


@pytest.mark.usefixtures("educational_level")
async def test_returns_valid_schema(api_client: httpx.AsyncClient) -> None:
    response = await api_client.get("educational-levels")
    assert response.status_code == status_codes.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) > 0
    [EducationalLevelResponse.model_validate(schema) for schema in response.json()]
