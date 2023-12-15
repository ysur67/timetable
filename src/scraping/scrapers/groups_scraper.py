from scraping.clients.groups_client import GroupsClient
from scraping.schemas.educational_level import EducationalLevelSchema


class GroupsScraper:
    def __init__(self, client: GroupsClient) -> None:
        self._client = client

    async def scrape(self) -> None:
        groups = await self._client.get_all(
            EducationalLevelSchema(title="asdf", code=""),
        )
        print(groups)  # noqa: T201
