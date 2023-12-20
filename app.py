from fastapi import FastAPI
from core.config.var_config import IS_PROD

app_desc = f"""
### 술술 REST API 문서입니다  
열심히 개발중이에요  

**대충 진행상황**
- 회원가입 플로우에 있는 '없는 안주 등록 요청' api 추가 > GET /pairings/requests
- 피드 검색 api 추가 but, mvp 검색은 pairing 검색이므로 일단 사용 x
- 이미지 업로드 api 추가 (S3에 저장 됩니다.) > POST /files/upload


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

# 절대 삭제하지 말것
from api.config.app_config import *

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app:app",
        port=8000,
        reload=True,
    )
