from pydantic import BaseModel

from core.domain.report_model import Report


class ReportRegisterRequest(BaseModel):
    reason: str
    type: str  # feed, comment
    target_id: int  # feed_id, comment_id


class ReportRegisterResponse(BaseModel):
    id: int
    reporter_id: int
    type: str
    target_id: int
    reason: str

    @classmethod
    def from_orm(cls, entity: Report):
        return ReportRegisterResponse(
            id=entity.id,
            type=entity.type,
            reporter_id=entity.reporter.id,
            target_id=entity.target_id,
            reason=entity.reason,
        )
