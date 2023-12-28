from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse

from api.config.middleware import auth_required
from core.config.orm_config import transactional
from core.domain.report.report_model import Report
from core.domain.user.user_model import User
from core.dto.report_dto import ReportRegisterResponse, ReportRegisterRequest

router = APIRouter(
    prefix="/reports",
    tags=["Report (신고)"],
)


@router.post(
    "", dependencies=[Depends(transactional)], response_model=ReportRegisterResponse
)
@auth_required
async def register_report(request: Request, request_body: ReportRegisterRequest):
    login_user = User.get_by_id(request.state.token_info["id"])
    report = Report.create(
        reporter=login_user,
        type=request_body.type,
        target_id=request_body.target_id,
        reason=request_body.reason,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ReportRegisterResponse.from_orm(report).model_dump(),
    )
