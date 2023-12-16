from collections.abc import Sequence
from typing import Final, Protocol, final

import httpx
from selectolax.parser import HTMLParser

from scraping.schemas.educational_level import EducationalLevelSchema
from scraping.schemas.group import GroupSchema


class GroupsClient(Protocol):
    async def get_all(self, level: EducationalLevelSchema) -> Sequence[GroupSchema]:
        ...


@final
class HttpGroupsClient(GroupsClient):
    BASE_URL: Final = "http://inet.ibi.spb.ru/raspisan/menu.php"

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_all(self, level: EducationalLevelSchema) -> Sequence[GroupSchema]:
        url = f"{self.BASE_URL}?tmenu={12}&cod={level.code}"
        response = await self._client.get(url)
        return self._scrape_groups(HTMLParser(response.text))

    def _scrape_groups(self, parser: HTMLParser) -> Sequence[GroupSchema]:
        result: list[GroupSchema] = []
        for node in parser.tags("option"):
            title = node.text(deep=False).strip()
            code = node.attributes.get("value", "UNDEFINED_CODE")
            if title:
                result.append(GroupSchema(title=title, code=code))
        return result


@final
class DummyGroupsClient(GroupsClient):
    def __init__(self, response_size: int) -> None:
        self.size: Final = response_size

    async def get_all(
        self,
        level: EducationalLevelSchema,  # noqa: ARG002
    ) -> Sequence[GroupSchema]:
        return [
            GroupSchema(title=f"Group: {index}", code=str(index))
            for index in range(self.size)
        ]
