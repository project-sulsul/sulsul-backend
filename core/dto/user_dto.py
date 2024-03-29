from typing import Dict, List, Optional

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
    nickname: str
    image: Optional[str]
    preference: Dict[str, List]
    status: str


class UserSimpleInfoResponse(BaseDTO):
    user_id: int
    nickname: str
    image: Optional[str]
