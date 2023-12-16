from collections.abc import Iterable
from typing import Any

import aioinject

from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.impls.neo.domain.educational_level.repositories import (
    NeoEducationalLevelRepository,
)
from core.impls.neo.domain.group.repositories import NeoGroupRepository

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Callable(NeoEducationalLevelRepository, type_=EducationalLevelRepository),
    aioinject.Callable(NeoGroupRepository, type_=GroupRepository),
]
