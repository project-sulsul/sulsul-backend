from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from core.domain.comment.comment_model import Comment
from core.dto.user_dto import UserSimpleInfoResponse


class CommentCreateRequest(BaseModel):
    content: str
    parent_comment_id: Optional[int] = None


class CommentUpdateRequest(BaseModel):
    content: str


class CommentResponse(BaseModel):
    comment_id: int
    user_info: UserSimpleInfoResponse
    content: str
    created_at: datetime
    updated_at: datetime
    is_reported: bool = False
    is_writer: bool = False
    is_deleted: bool = False
    parent_comment_id: Optional[int] = None
    children_comments: Optional[List["CommentResponse"]]

    @classmethod
    def of_dto(
        cls,
        comment: "CommentDto",
        children_comments: List["CommentResponse"] = None,
        is_writer=False,
    ):
        return CommentResponse(
            **dict(comment),
            comment_id=comment.id,
            user_info=UserSimpleInfoResponse(
                user_id=comment.user,
                nickname=comment.nickname,
                image=comment.image,
            ),
            parent_comment_id=comment.parent_comment,
            is_writer=is_writer,
            children_comments=children_comments,
        )

    @classmethod
    def of(
        cls,
        comment: Comment,
        parent_comment_id: Optional[int] = None,
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
            parent_comment_id=parent_comment_id,
            is_writer=is_writer,
            children_comments=children_comments,
        )


class CommentListResponse(BaseModel):
    comments: List[CommentResponse]


class CommentDto(BaseModel):
    id: int  # comment_id
    user: int  # user_id
    feed: int  # feed_id
    content: str
    parent_comment: Optional[int]  # parent_comment_id
    is_reported: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    nickname: str  # user_nickname
    image: Optional[str]  # user_profile_image
