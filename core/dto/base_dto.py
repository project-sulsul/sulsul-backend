from typing import List, T, Optional

from pydantic import BaseModel


class BaseDTO(BaseModel):
    @classmethod
    def from_orm(cls, entity):
        return cls(**entity.__data__)


class CursorPageRequest(BaseModel):
    next_cursor_id: Optional[int] = None
    size: int = 6
    sort: Optional[str] = None
    direction: str = "asc"


class CursorPageResponse(BaseModel):
    next_cursor_id: Optional[int]
    size: int
    is_last: bool
    content: Optional[list]
