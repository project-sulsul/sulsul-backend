from datetime import datetime

from pydantic import BaseModel

from core.domain.report.report_model import Report


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
    def of(cls, report: Report):
        return ReportRegisterResponse(reporter_id=report.reporter.id, **report.__data__)


class ReportResponse(BaseModel):
    id: int
    reporter_id: int
    type: str
    target_id: int
    reason: str
    status: str
    created_at: datetime

    @classmethod
    def of(cls, report: Report):
        return ReportResponse(reporter_id=report.reporter.id, **report.__data__)
