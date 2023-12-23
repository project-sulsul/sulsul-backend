from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from core.domain.comment_model import Comment
from core.dto.user_dto import UserSimpleInfoResponse


class CommentCreateRequest(BaseModel):
    content: str
    parent_comment_id: Optional[int] = None


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

    @classmethod
    def of(
        cls,
        comment: Comment,
        children_comments: List["CommentResponse"] = None,
        is_writer=False,
    ):
        return CommentResponse(
            **comment.__data__,
            comment_id=comment.id,
            user_info=UserSimpleInfoResponse(
                user_id=comment.user.id,
                nickname=comment.user.nickname,
                image=comment.user.image,
            ),
            is_writer=is_writer,
            children_comments=children_comments,
        )


class CommentListResponse(BaseModel):
    comments: List[CommentResponse]
