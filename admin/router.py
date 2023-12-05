from fastapi import APIRouter, Depends, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, PlainTextResponse

import bcrypt
from datetime import datetime

from api.config.middleware import admin
from core.util.jwt import build_token
from core.config.orm_config import transactional
from admin.model import Admin, AdminSigninModel
from core.config.var_config import KST, TOKEN_TYPE, TOKEN_DURATION, JWT_COOKIE_OPTIONS
from core.domain.pairing_model import Pairing
from core.dto.pairing_dto import PairingCreateModel, PairingUpdateModel, PairingAdminResponseModel


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    include_in_schema=False,
)

templates = Jinja2Templates(directory="admin/templates")


@router.get("/sign-in")
async def admin_sign_in_template(request: Request):
    return templates.TemplateResponse("admin_sign_in.html", {"request": request})


@router.get("")
@admin
async def admin_index_template(request: Request):
    return templates.TemplateResponse("admin_index.html", {"request": request})


@router.get("/pairing")
@admin
async def admin_pairing_template(request: Request):
    return templates.TemplateResponse("admin_pairing.html", {"request": request})


@router.get("/user")
@admin
async def admin_user_template(request: Request):
    return templates.TemplateResponse("admin_user.html", {"request": request})


@router.get("/feed")
@admin
async def admin_feed_template(request: Request):
    return templates.TemplateResponse("admin_feed.html", {"request": request})


@router.get("/comment")
@admin
async def admin_comment_template(request: Request):
    return templates.TemplateResponse("admin_comment.html", {"request": request})


@router.get("/report")
@admin
async def admin_report_template(request: Request):
    return templates.TemplateResponse("admin_report.html", {"request": request})


@router.post("/sign-in", dependencies=[Depends(transactional)])
async def admin_sign_in(request: Request, form: AdminSigninModel):
    form = form.model_dump()
    admin = Admin.select().first()
    if form["username"] == admin.username and bcrypt.checkpw(
        form["password"].encode("utf-8"), admin.password.encode("utf-8")
    ):
        token = build_token(id=admin.id, is_admin_token=True)
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"token_type": TOKEN_TYPE, "access_token": token},
        )
        response.set_cookie(value=token, max_age=TOKEN_DURATION, **JWT_COOKIE_OPTIONS)
        return response

    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Incorrect credentials"},
        )


@router.delete("/sign-out")
async def admin_sign_out(request: Request):
    response = PlainTextResponse("logout")
    response.delete_cookie("access_token")
    return response


@router.get("/pairings")
@admin
async def get_pairings(request: Request):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            PairingAdminResponseModel.from_orm(pairing).model_dump()
            for pairing in Pairing.select().order_by(Pairing.id)
        ],
    )


@router.post("/pairings")
@admin
async def create_pairing(request: Request, form: PairingCreateModel):
    form = form.model_dump()
    pairing = Pairing.create(**form)
    return JSONResponse(status_code=status.HTTP_200_OK, content=PairingAdminResponseModel.from_orm(pairing).model_dump())


@router.put("/pairings/{pairing_id}")
@admin
async def update_pairing(request: Request, pairing_id: int, form: PairingUpdateModel):
    form = form.model_dump()
    pairing = (
        Pairing.update(
            updated_at=datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z"), **form
        )
        .where(Pairing.id == pairing_id)
        .execute()
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
