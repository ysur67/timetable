from scraping.schemas.base import BaseSchema


class GroupSchema(BaseSchema):
    title: str
    code: str


class GroupWithoutCodeSchema(BaseSchema):
    title: str
