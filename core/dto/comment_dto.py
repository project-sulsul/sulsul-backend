from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from core.dto.user_dto import UserSimpleInfoResponse


class CommentResponse(BaseModel):
    comment_id: int
    user_info: UserSimpleInfoResponse
    content: str
    created_at: datetime
    updated_at: datetime
    is_reported: bool = False
    is_writer: bool = False
    children_comments: Optional[List["CommentResponse"]]

    @classmethod
    def of_dict(
        cls,
        comment: dict,
        children_comments: List["CommentResponse"] = None,
        is_writer=False,
    ):
        return CommentResponse(
            **comment,
            comment_id=comment["id"],
            user_info=UserSimpleInfoResponse(
                user_id=comment["user"],
                nickname=comment["nickname"],
                image=comment["image"],
            ),
            is_writer=is_writer,
            children_comments=children_comments,
        )


class CommentListResponse(BaseModel):
    comments: List[CommentResponse]
