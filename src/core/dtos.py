from pydantic import BaseModel, ConfigDict


class BaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PaginationDto(BaseDto):
    page: int
    page_size: int

    def get_offset(self) -> int:
        if self.page > 1:
            return self.page * self.page_size
        return 0
