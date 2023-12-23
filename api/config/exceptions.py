from fastapi import HTTPException
from starlette import status


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "forbidden."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
