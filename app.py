from fastapi import FastAPI


app_desc = """
### 술술 REST API 문서입니다  
열심히 개발중이에요  

**대충 진행상황**
- 데이터베이스가 추가됐어요
- 유저 테이블이 추가됐어요
- 구글 로그인은 어느정도 완성되었고 테스트 해보시면 돼요  
- 카카오 로그인은 아직 개발 중이에요
"""
app = FastAPI(
    title="술술 API",
    description=app_desc,
    version="0.0.1",
    contact={"name": "tmlee", "email": "ahdwjdtprtm@gmail.com"},
    license_info={"name": "MIT License", "identifier": "MIT"}
)


from src.config.app_config import *


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="app:app",
        port=8000,
        reload=True,
    )
