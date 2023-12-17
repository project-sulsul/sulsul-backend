from typing import Dict, List
from pydantic import BaseModel

from core.domain.user_model import User


class NicknameResponse(BaseModel):
    nickname: str


class NicknameValidationResponse(BaseModel):
    is_valid: bool
    message: str | None


class UserNicknameUpdateRequest(BaseModel):
    nickname: str


class UserPreferenceUpdateRequest(BaseModel):
    preference: Dict[str, List]


class UserResponse(BaseModel):
    id: int
    uid: str
    nickname: str
    preference: Dict[str, List]
    status: str

    @classmethod
    def from_orm(cls, entity: User):
        return UserResponse(
            id=entity.id,
            uid=entity.uid,
            nickname=entity.nickname,
            preference=entity.preference,
            status=entity.status,
        )


class UserSimpleInfoResponse(BaseModel):
    user_id: int
    nickname: str
