from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.domain.comment_model import Comment
from core.domain.user_model import User
from core.dto.user_dto import UserSimpleInfoResponse


class CommentResponse(BaseModel):
    comment_id: int
    user_info: UserSimpleInfoResponse
    content: str
    created_at: datetime
    updated_at: datetime
    is_reported: bool = False
    is_writer: bool = False
    children_comments: List["CommentResponse"] | None

    @classmethod
    def of_dict(cls, comment: dict, children_comments=None, is_writer=False):
        return CommentResponse(
            comment_id=comment["id"],
            user_info=UserSimpleInfoResponse(
                user_id=comment["user"],
                nickname=comment["nickname"],
                image=comment["image"],
            ),
            content=comment["content"],
            created_at=comment["created_at"],
            updated_at=comment["updated_at"],
            is_reported=comment["is_reported"],
            children_comments=children_comments,
        )


class CommentListResponse(BaseModel):
    comments: List[CommentResponse]
