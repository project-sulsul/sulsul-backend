from typing import List, T

from pydantic import BaseModel


class BaseDTO(BaseModel):
    @classmethod
    def from_orm(cls, entity):
        return cls(**entity.__data__)


class CursorPageRequest(BaseModel):
    next_cursor_id: int | None = None
    size: int = 6
    sort: str | None = None
    direction: str = "asc"


class CursorPageResponse(BaseModel):
    next_cursor_id: int | None
    size: int
    is_last: bool
    content: list | None
