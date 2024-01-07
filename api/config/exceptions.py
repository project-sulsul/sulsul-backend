from fastapi import HTTPException
from starlette import status


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "forbidden."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotFoundException(HTTPException):
    def __init__(self, target_entity, target_id: int, detail: str = "not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{target_entity.__name__}(id:{target_id}) {detail}",
        )


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "unauthorized."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
