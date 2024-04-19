import pytest

from core.domain.group.queries.get_groups_query import GetGroupsQuery, GroupsFilter
from core.models.educational_level import EducationalLevel


async def test_returns_nothing_if_there_are_no_groups(
    get_groups_query: GetGroupsQuery,
    educational_level: EducationalLevel,
) -> None:
    result = await get_groups_query.execute(GroupsFilter(educational_level_id=educational_level.id))
    assert len(result) == 0


@pytest.mark.usefixtures("group")
async def test_returns_actual_group_if_such_group_belongs_to_educational_level(
    get_groups_query: GetGroupsQuery,
    educational_level: EducationalLevel,
) -> None:
    result = await get_groups_query.execute(GroupsFilter(level_id=educational_level.id))
    assert len(result) == 1
    assert result[0].level_id == educational_level.id
