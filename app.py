from fastapi import FastAPI
from core.config.var_config import IS_PROD


app_desc = f"""
### 술술 REST API 문서입니다  
열심히 개발중이에요  

**대충 진행상황**
- 데이터베이스가 추가됐어요
- 유저 테이블이 추가됐어요
- 구글, 카카오 로그인은 어느정도 완성되었고 테스트 해보시면 돼요
- 애플 로그인은 개발 중이에요
- 회원 기능 일부가 추가되었어요. (유저 조회, 닉네임/취향 변경)
- 술/안주(Pairing) 조회 기능이 추가됐어요
- 관리자 페이지는 개발 중이에요.(/admin)

**몇가지 사용법**
- 로그인이 필요한 API는 '<token_type> <access_token>' 형태의 값을 Authorization 헤더에 포함하여 요청합니다.

[**관리자 페이지**]({'http://sulsul-env.eba-gvmvk4bq.ap-northeast-2.elasticbeanstalk.com/admin' if IS_PROD else 'http://localhost:8000/admin'})
"""
app = FastAPI(
    title="술술 API",
    description=app_desc,
    version="0.0.1",
    contact={"name": "tmlee", "email": "ahdwjdtprtm@gmail.com"},
    license_info={"name": "MIT License", "identifier": "MIT"},
)


from api.config.app_config import *


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app:app",
        port=8000,
        reload=True,
    )
