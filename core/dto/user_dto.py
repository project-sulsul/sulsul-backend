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
    """
    유저 취향 수정 모델
    - alcohol (List[int]): 취향으로 등록할 술(pairing)들의 ID 목록
    - foods (List[int]): 취향으로 등록할 안주(pairing)들의 ID 목록
    """

    alcohol: List[int]
    foods: List[int]


class UserResponse(BaseModel):
    id: int
    uid: str
    nickname: str
    image: str
    preference: Dict[str, List]
    status: str

    @classmethod
    def from_orm(cls, entity: User):
        return UserResponse(
            id=entity.id,
            uid=entity.uid,
            nickname=entity.nickname,
            image=entity.image,
            preference=entity.preference,
            status=entity.status,
        )


class UserSimpleInfoResponse(BaseModel):
    user_id: int
    nickname: str
    image: str
