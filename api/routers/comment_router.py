from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from api.config.middleware import auth
from core.config.orm_config import read_only
from core.domain.comment_model import Comment
from core.domain.user_model import User
from core.dto.comment_dto import CommentResponse, CommentListResponse
from core.util.auth_util import get_login_user_id

router = APIRouter(
    prefix="/feeds/{feed_id}/comments",
    tags=["Comment"],
)


@router.get(
    "",
    dependencies=[Depends(read_only)],
    response_model=CommentListResponse,
)
@auth
async def get_all_comments_of_feed(request: Request, feed_id: int):
    comments = (
        Comment.select(Comment, User)
        .join(User)
        .where((Comment.feed == feed_id) & (Comment.is_deleted == False))
        .dicts()
    )

    parent_comments = [
        comment for comment in comments if comment["parent_comment"] is None
    ]
    parent_to_children = {comment["id"]: [] for comment in parent_comments}

    for comment in comments:
        if comment["parent_comment"] is not None:
            parent_to_children[comment["parent_comment"]].append(comment)

    result = build_comment_hierarchy(request, parent_comments, parent_to_children)
    return CommentListResponse(comments=result)


def build_comment_hierarchy(
    request: Request, parent_comments: List[dict], parent_to_children: dict
) -> List[CommentResponse]:
    result = []
    login_user_id = get_login_user_id(request)

    for parent_comment in parent_comments:
        parent_id = parent_comment["id"]
        children_comments = build_children_comments(
            parent_to_children[parent_id], login_user_id
        )
        is_writer = parent_comment["user"] == login_user_id

        parent_comment_response = CommentResponse.of_dict(
            comment=parent_comment,
            children_comments=children_comments,
            is_writer=is_writer,
        )

        result.append(parent_comment_response)

    return result


def build_children_comments(
    children_data: List[dict], login_user_id: int
) -> List[CommentResponse]:
    children_comments = []

    for child_dict in children_data:
        is_writer = child_dict["user"] == login_user_id
        child_comment = CommentResponse.of_dict(comment=child_dict, is_writer=is_writer)
        children_comments.append(child_comment)

    return children_comments
