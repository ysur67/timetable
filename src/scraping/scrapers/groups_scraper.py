import uuid
from collections.abc import Iterable
from dataclasses import dataclass

from core.domain.educational_level.repositories import EducationalLevelRepository
from core.domain.group.repositories import GroupRepository
from core.models import EducationalLevel, Group, GroupId
from lib.logger import get_default_logger
from scraping.clients.groups.groups_client import GroupsClient
from scraping.schemas.educational_level import EducationalLevelSchema
from scraping.schemas.group import GroupSchema


@dataclass(frozen=True)
class _GroupKey:
    title: str
    level: EducationalLevel


@dataclass
class _ExtractGroupsResponse:
    existing: dict[_GroupKey, GroupSchema]
    to_create: dict[_GroupKey, GroupSchema]


class GroupsScraper:
    def __init__(
        self,
        client: GroupsClient,
        educational_level_repository: EducationalLevelRepository,
        groups_repository: GroupRepository,
    ) -> None:
        self._client = client
        self._educational_level_repo = educational_level_repository
        self._group_repo = groups_repository
        self._logger = get_default_logger(self.__class__.__name__)

    async def scrape(self) -> None:
        self._logger.info("Starting %s...", self.__class__.__name__)
        educational_levels = await self._educational_level_repo.get_all()
        response = await self._extract_groups(educational_levels)
        # TODO: Implement removal of outdated groups
        await self._group_repo.create_bulk(
            [
                Group(
                    id=GroupId(uuid.uuid4()),
                    title=schema.title,
                    level=key.level,
                    external_id=schema.code,
                )
                for key, schema in response.to_create.items()
            ],
        )

    async def _extract_groups(
        self,
        educational_levels: Iterable[EducationalLevel],
    ) -> _ExtractGroupsResponse:
        groups = await self._group_repo.get_all()
        existing: dict[_GroupKey, GroupSchema] = {
            _GroupKey(title=group.title, level=group.level): GroupSchema(
                title=group.title,
                code=group.external_id,
            )
            for group in groups
        }
        to_create: dict[_GroupKey, GroupSchema] = {}
        for level in educational_levels:
            self._logger.info(
                "Trying to find groups for %s: %s...",
                EducationalLevel.__name__,
                level.title,
            )
            found_groups = await self._client.get_all(
                EducationalLevelSchema(
                    title=level.title,
                    code=level.code,
                ),
            )
            self._logger.info("Found %d groups", len(found_groups))
            for group in found_groups:
                key = _GroupKey(title=group.title, level=level)
                if (existing.get(key)) is None:
                    self._logger.info(
                        "Found new %s: %s",
                        Group.__name__,
                        group.title,
                    )
                    to_create[key] = group
        return _ExtractGroupsResponse(
            existing=existing,
            to_create=to_create,
        )
