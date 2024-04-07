from fastapi import APIRouter, Request, Depends

from api.config.exceptions import BadRequestException
from api.descriptions.report_api_descriptions import REGISTER_REPORT_DESC
from api.descriptions.responses_dict import UNAUTHORIZED_RESPONSE, NOT_FOUND_RESPONSE, BAD_REQUEST_RESPONSE
from core.config.orm_config import transactional
from core.domain.comment.comment_model import Comment
from core.domain.feed.feed_model import Feed
from core.domain.report.report_model import Report, ReportStatus
from core.domain.user.user_model import User
from core.dto.report_dto import ReportRegisterResponse, ReportRegisterRequest
from core.util.auth_util import get_login_user_id, AuthRequired

router = APIRouter(
    prefix="/reports",
    tags=["Report (신고)"],
)


@router.post(
    "",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=ReportRegisterResponse,
    description=REGISTER_REPORT_DESC,
    responses={**UNAUTHORIZED_RESPONSE, **NOT_FOUND_RESPONSE, **BAD_REQUEST_RESPONSE},
)
async def register_report(request: Request, request_body: ReportRegisterRequest):
    login_user = User.get_or_raise(get_login_user_id(request))

    if len(request_body.reason) > 500:
        raise BadRequestException("신고 사유는 500자 이하로 입력해주세요.")

    report = Report.create(
        reporter=login_user,
        type=request_body.type,
        target_id=request_body.target_id,
        reason=request_body.reason,
        status=ReportStatus.PENDING.name,
    )

    if request_body.type == "feed":
        if Feed.get_or_none(id=request_body.target_id) is None:
            raise BadRequestException(f"({request_body.target_id}) 존재하지 않는 피드입니다.")
        Feed.update(is_reported=True).where(Feed.id == request_body.target_id).execute()

    elif request_body.type == "comment":
        if Comment.get_or_none(id=request_body.target_id) is None:
            raise BadRequestException(f"({request_body.target_id}) 존재하지 않는 댓글입니다.")
        Comment.update(is_reported=True).where(
            Comment.id == request_body.target_id
        ).execute()

    else:
        raise BadRequestException("type은 feed 또는 comment만 가능합니다.")

    return ReportRegisterResponse.of(report)
