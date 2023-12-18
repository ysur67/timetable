import pytest

from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.models import EducationalLevel

pytestmark = [pytest.mark.anyio]


async def test_returns_actual_data_if_there_are_existing_educational_levels(
    get_all_educational_levels_query: GetAllEducationalLevelsQuery,
    educational_level: EducationalLevel,
) -> None:
    result = await get_all_educational_levels_query.execute()
    assert len(result) == 1
    assert result[0].id == educational_level.id


async def test_returns_nothing_if_there_is_no_educational_levels(
    get_all_educational_levels_query: GetAllEducationalLevelsQuery,
) -> None:
    result = await get_all_educational_levels_query.execute()
    assert len(result) == 0
