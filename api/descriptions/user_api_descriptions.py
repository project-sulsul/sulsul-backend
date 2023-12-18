from core.config.var_config import USER_NICKNAME_MAX_LENGTH

GENERATE_RANDOM_NICKNAME_DESC = f"""
### 임의의 닉네임을 생성
**로그인이 필요한 API 입니다.**  
닉네임 최대 길이 {USER_NICKNAME_MAX_LENGTH}자 아내 특수문자가 포함되지 않은 닉네임을 반환합니다.
"""

GET_USER_BY_ID_DESC = """
### ID로 유저 정보를 조회
"""

VALIDATE_USER_NICKNAME_DESC = f"""
### 닉네임의 유효성 검증
**로그인이 필요한 API 입니다.**  
닉네임 최대 길이({USER_NICKNAME_MAX_LENGTH}자)와 특수문자 포함 여부, 중복을 검증합니다.
"""

UPDATE_USER_NICKNAME_DESC = """
### 유저 닉네임 변경
**로그인이 필요한 API 입니다.**  
로그인 한 유저 본인의 닉네임만 변경 가능합니다.
"""

UPDATE_USER_IMAGE_DESC = """
### 유저 프로필 사진 변경
**로그인이 필요한 API 입니다.**
로그인 한 유저 본인의 프로필 사진만 변경 가능합니다
"""

UPDATE_USER_PREFERENCE_DESC = """
### 유저 취향 변경
**로그인이 필요한 API 입니다.**  
로그인 한 유저 본인의 취향만 변경 가능합니다.
"""

DELETE_USER_DESC = """
### 유저 삭제
**로그인이 필요한 API 입니다.**  
로그인 한 유저 본인만 삭제 가능합니다.
"""
