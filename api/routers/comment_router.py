from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from api.descriptions.responses_dict import NOT_FOUND_RESPONSE, UNAUTHORIZED_RESPONSE
from core.config.orm_config import read_only, transactional
from core.domain.comment.comment_model import Comment
from core.domain.feed.feed_model import Feed
from core.domain.user.user_model import User
from core.dto.comment_dto import (
    CommentResponse,
    CommentListResponse,
    CommentCreateRequest,
    CommentUpdateRequest,
    CommentDto,
)
from core.util.auth_util import get_login_user_id, AuthRequired, AuthOptional
from core.util.comment_util import CommentBuilder

router = APIRouter(
    prefix="/feeds/{feed_id}/comments",
    tags=["Comment"],
)


@router.post(
    "",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=CommentResponse,
    responses={**NOT_FOUND_RESPONSE, **UNAUTHORIZED_RESPONSE},
)
async def create_comment(
    request: Request, feed_id: int, request_body: CommentCreateRequest
):
    Feed.get_or_raise(feed_id)
    request_body.validate_input()

    login_user = User.get_or_raise(get_login_user_id(request))
    if request_body.parent_comment_id is not None:
        Comment.get_or_raise(request_body.parent_comment_id)
        comment = Comment.create(
            user=login_user,
            feed=feed_id,
            content=request_body.content,
            parent_comment=request_body.parent_comment_id,
        )
    else:
        comment = Comment.create(
            user=login_user,
            feed=feed_id,
            content=request_body.content,
        )

    return CommentResponse.of(
        comment=comment,
        parent_comment_id=request_body.parent_comment_id,
        is_writer=True,
    )


@router.put(
    "/{comment_id}",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=CommentResponse,
    responses={**NOT_FOUND_RESPONSE, **UNAUTHORIZED_RESPONSE},
)
async def update_comment(
    request: Request, feed_id: int, comment_id: int, request_body: CommentUpdateRequest
):
    Feed.get_or_raise(feed_id)
    request_body.validate_input()

    comment = Comment.get_or_raise(comment_id)

    comment.check_if_owner(get_login_user_id(request))

    comment.update_content(request_body.content)

    return CommentResponse.of(
        comment=comment,
        is_writer=True,
    )


@router.delete(
    "/{comment_id}",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=CommentResponse,
    responses={**NOT_FOUND_RESPONSE, **UNAUTHORIZED_RESPONSE},
)
async def soft_delete_comment(request: Request, feed_id: int, comment_id: int):
    Feed.get_or_raise(feed_id)

    comment = Comment.get_or_raise(comment_id)
    comment.check_if_owner(get_login_user_id(request))

    comment.soft_delete()

    return CommentResponse.of(
        comment=comment,
        is_writer=True,
    )


@router.get(
    "",
    dependencies=[Depends(read_only), Depends(AuthOptional())],
    response_model=CommentListResponse,
)
async def get_all_comments_of_feed(request: Request, feed_id: int):
    comments: List[CommentDto] = (
        Comment.select(Comment, User)
        .join(User)
        .where(Comment.feed == feed_id)
        .objects(constructor=CommentDto)
    )

    result = CommentBuilder.layering(get_login_user_id(request), comments)

    return CommentListResponse(comments=result)
