from fastapi import APIRouter, Depends, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from src.middleware import admin
from src.jwt import build_token
from src.orm import transactional
from admin.model import Admin, AdminSigninModel
from src.config.var_config import ADMIN_JWT_COOKIE_OPTIONS


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    include_in_schema=False,
)

templates = Jinja2Templates(directory="templates")


@router.get("")
@admin
async def admin_index_template(request: Request):
    return templates.TemplateResponse("admin_index.html", {"request": request})


@router.get("/sign-in")
async def admin_sign_in_template(request: Request):
    return templates.TemplateResponse("admin_sign_in.html", {"request": request})


@router.post("/sign-in", dependencies=[Depends(transactional)])
async def admin_sign_in(request: Request, form: AdminSigninModel):
    form = form.model_dump()
    admin = Admin.select().first()
    if form["username"] == admin.username and form["password"] == admin.password:
        token = build_token(
            id=admin.id,
            is_admin_token=True,
        )
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"token_type": "Bearer", "access_token": token}
        )
        response.set_cookie(value=token, **ADMIN_JWT_COOKIE_OPTIONS)
        return response
    
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Incorrect credentials"},
        )

