import pytest

from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.domain.group.repositories import GroupRepository
from core.impls.neo.domain.educational_level.queries.get_all import (
    NeoGetAllEducationalLevelsQuery,
)
from core.impls.neo.domain.group.queries.get_by_educational_level import (
    NeoGetGroupsByEducationalLevelQuery,
)


@pytest.fixture()
def get_all_educational_levels_query(
    educational_level_repository: EducationalLevelRepository,
) -> GetAllEducationalLevelsQuery:
    return NeoGetAllEducationalLevelsQuery(educational_level_repository)


@pytest.fixture()
def get_groups_by_educational_level_query(
    group_repository: GroupRepository,
) -> GetGroupsByEducationalLevelQuery:
    return NeoGetGroupsByEducationalLevelQuery(group_repository)
