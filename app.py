from fastapi import FastAPI
from core.config.var_config import IS_PROD

app_desc = f"""
### 술술 REST API 문서입니다  
*로그인 필수*라고 붙은 것은 jwt 토큰이 없으면 401 에러가 납니다.

**몇 가지 사용법**
- 로그인이 필요한 API는 '<token_type> <access_token>' 형태의 값을 Authorization 헤더에 포함하여 요청합니다.
- 테스트용 API 중 jwt를 사용하면 개발용 jwt를 발급받을 수 있습니다. (user_id: 1)
- AuthRequired - 로그인 필수
- AuthOptional - 로그인 선택 (로그인 안 해도 리턴 됨. 로그인 하면 추가 동작을 함. ex. 로그인 사용자 좋아요 표시)

[**관리자 페이지**]({'http://sulsul-env.eba-gvmvk4bq.ap-northeast-2.elasticbeanstalk.com/admin' if IS_PROD else 'http://localhost:8000/admin'})
"""
app = FastAPI(
    title="술술 API",
    description=app_desc,
    version="0.0.1",
    contact={"name": "tmlee", "email": "ahdwjdtprtm@gmail.com"},
    license_info={"name": "MIT License", "identifier": "MIT"},
)

# 절대 삭제하지 말것
from api.config.app_config import *

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app:app",
        port=8000,
        reload=True,
    )
