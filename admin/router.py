from datetime import datetime
from typing import Optional

import bcrypt
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

from admin.model import Admin, AdminSigninModel
from api.config.middleware import admin
from core.config.orm_config import transactional, read_only
from core.config.var_config import KST, TOKEN_TYPE, TOKEN_DURATION, JWT_COOKIE_OPTIONS
from core.domain.pairing.pairing_model import Pairing
from core.domain.report.report_model import Report, ReportStatus
from core.dto.page_dto import NormalPageResponse
from core.dto.pairing_dto import (
    PairingCreateRequest,
    PairingUpdateRequest,
    PairingAdminResponse,
)
from core.dto.report_dto import ReportResponse
from core.util.jwt import build_token

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
            PairingAdminResponse.from_orm(pairing).model_dump()
            for pairing in Pairing.select().order_by(Pairing.id)
        ],
    )


@router.post("/pairings")
@admin
async def create_pairing(request: Request, form: PairingCreateRequest):
    form = form.model_dump()
    pairing = Pairing.create(**form)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=PairingAdminResponse.from_orm(pairing).model_dump(),
    )


@router.put("/pairings/{pairing_id}")
@admin
async def update_pairing(request: Request, pairing_id: int, form: PairingUpdateRequest):
    form = form.model_dump()
    pairing = (
        Pairing.update(
            updated_at=datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S%z"), **form
        )
        .where(Pairing.id == pairing_id)
        .execute()
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content={})


"""
신고 ADMIN API
"""


@router.get(
    "/reports",
    dependencies=[Depends(read_only)],
    response_model=NormalPageResponse,
)
@admin
async def get_all_reports(
    request: Request,
    report_status: Optional[ReportStatus] = None,
    page: int = 0,
    size: int = 10,
):
    if report_status:
        query = Report.select().where(Report.status == report_status)
        total_count = query.count()
        reports = query.paginate(page, size)
    else:
        total_count = Report.select().count()
        reports = Report.select().paginate(page, size)
    return NormalPageResponse(
        total_count=total_count,
        size=size,
        is_last=(page + 1) * size >= total_count,
        content=[ReportResponse.of(report) for report in reports],
    )


@router.get(
    "/reports/{report_id}",
    dependencies=[Depends(read_only)],
    response_model=ReportResponse,
)
@admin
async def get_report_detail(
    request: Request,
    report_id: int,
):
    return ReportResponse.of(Report.get_or_raise(report_id))


@router.put(
    "/reports/{report_id}/status",
    dependencies=[Depends(transactional)],
    response_model=ReportResponse,
)
@admin
async def update_report_status(
    request: Request,
    report_id: int,
    report_status: ReportStatus,
):
    Report.update(status=report_status).where(Report.id == report_id).execute()
