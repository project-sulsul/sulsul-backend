from typing import Dict, List
from pydantic import BaseModel

from core.domain.user_model import User


class NicknameResponseModel(BaseModel):
    nickname: str


class NicknameValidationResponseModel(BaseModel):
    is_valid: bool
    message: str | None


class UserNicknameUpdateModel(BaseModel):
    nickname: str


class UserPreferenceUpdateModel(BaseModel):
    preference: Dict[str, List]


class UserResponseModel(BaseModel):
    id: int
    uid: str
    nickname: str
    preference: Dict[str, List]
    status: str

    @classmethod
    def from_orm(cls, entity: User):
        return UserResponseModel(
            id=entity.id,
            uid=entity.uid,
            nickname=entity.nickname,
            preference=entity.preference,
            status=entity.status,
        )
