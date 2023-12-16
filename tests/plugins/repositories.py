import pytest
from neo4j import AsyncSession

from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.impls.neo.domain.educational_level.repositories import (
    NeoEducationalLevelRepository,
)
from core.impls.neo.domain.group.repositories import NeoGroupRepository


@pytest.fixture()
def group_repository(session: AsyncSession) -> GroupRepository:
    return NeoGroupRepository(session)


@pytest.fixture()
def educational_level_repository(session: AsyncSession) -> EducationalLevelRepository:
    return NeoEducationalLevelRepository(session)
