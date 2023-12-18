import pytest

from core.domain.group.dtos import GetGroupsByEducationalLevelDto
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.models.educational_level import EducationalLevel

pytestmark = [pytest.mark.anyio]


async def test_returns_nothing_if_there_are_no_groups(
    get_groups_by_educational_level_query: GetGroupsByEducationalLevelQuery,
    educational_level: EducationalLevel,
) -> None:
    result = await get_groups_by_educational_level_query.execute(
        GetGroupsByEducationalLevelDto(level_id=educational_level.id),
    )
    assert len(result) == 0


@pytest.mark.usefixtures("group")
async def test_returns_actual_group_if_such_group_belongs_to_educational_level(
    get_groups_by_educational_level_query: GetGroupsByEducationalLevelQuery,
    educational_level: EducationalLevel,
) -> None:
    result = await get_groups_by_educational_level_query.execute(
        GetGroupsByEducationalLevelDto(level_id=educational_level.id),
    )
    assert len(result) == 1
    assert result[0].level.id == educational_level.id
