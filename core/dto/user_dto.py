from datetime import datetime
from typing import Dict, List, Optional

from core.domain.user.user_model import UserStatus
from core.dto.base_dto import BaseDTO


class NicknameResponse(BaseDTO):
    nickname: str


class NicknameValidationResponse(BaseDTO):
    is_valid: bool
    message: Optional[str]


class UserNicknameUpdateRequest(BaseDTO):
    nickname: str


class UserPreferenceUpdateRequest(BaseDTO):
    """
    유저 취향 수정 모델
    - alcohol (List[int]): 취향으로 등록할 술(pairing)들의 ID 목록
    - foods (List[int]): 취향으로 등록할 안주(pairing)들의 ID 목록
    """

    alcohols: List[int]
    foods: List[int]


class UserResponse(BaseDTO):
    id: int
    uid: str
    nickname: Optional[str]
    image: Optional[str]
    preference: Dict[str, List]
    status: UserStatus


class UserSimpleInfoResponse(BaseDTO):
    user_id: int
    nickname: str
    image: Optional[str]


class UserAdminResponse(BaseDTO):
    id: int
    uid: str
    nickname: Optional[str]
    image: Optional[str]
    preference: Dict[str, List]
    social_type: Optional[str]
    device_type: Optional[str]
    status: UserStatus
    created_at: datetime
    updated_at: datetime


class UserAdminStatusUpdateRequest(BaseDTO):
    user_ids: List[int]
    status: UserStatus


class UserAdminNicknameUpdateRequest(BaseDTO):
    nickname: str


class UserBlockResponse(BaseDTO):
    target_user_id: int
