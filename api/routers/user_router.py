import re
import time

from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from peewee import DoesNotExist

from api.descriptions.user_api_descriptions import *
from core.client.nickname_generator_client import NicknameGeneratorClient
from core.config.orm_config import transactional, read_only
from core.domain.comment.comment_model import Comment
from core.domain.feed.feed_like_model import FeedLike
from core.domain.feed.feed_model import Feed
from core.domain.user.user_block_model import UserBlock
from core.domain.user.user_model import User
from core.dto.user_dto import NicknameResponse, UserBlockResponse
from core.dto.user_dto import NicknameValidationResponse
from core.dto.user_dto import UserNicknameUpdateRequest
from core.dto.user_dto import UserPreferenceUpdateRequest
from core.dto.user_dto import UserResponse
from core.util.auth_util import AuthRequired

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get(
    "/nickname",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=NicknameResponse,
    description=GENERATE_RANDOM_NICKNAME_DESC,
)
async def generate_random_nickname(request: Request):
    nicknames = NicknameGeneratorClient.generate_random_nickname()
    for nickname in nicknames:
        count = User.select().where(User.nickname == nickname).count()
        if (
                count == 0
                and not re.compile(r'[!@#$%^&*(),.?":{}|<>]').search(nickname)
                and len(nickname) <= USER_NICKNAME_MAX_LENGTH
        ):
            return NicknameResponse(nickname=nickname)


@router.get(
    "/{user_id}",
    dependencies=[Depends(read_only)],
    response_model=UserResponse,
    description=GET_USER_BY_ID_DESC,
)
async def get_user_by_id(user_id: int):
    user = User.get_or_none(User.id == user_id, User.is_deleted == False)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"User {user_id} doesn't exist"},
        )
    return UserResponse.from_orm(user)


@router.get(
    "/validation",
    dependencies=[Depends(read_only), Depends(AuthRequired())],
    response_model=NicknameValidationResponse,
    description=VALIDATE_USER_NICKNAME_DESC,
)
async def validate_user_nickname(request: Request, nickname: str):
    if len(nickname) > USER_NICKNAME_MAX_LENGTH:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=NicknameValidationResponse(
                is_valid=False,
                message=f"Max length({USER_NICKNAME_MAX_LENGTH}) exceeded",
            ).model_dump(),
        )
    if re.compile(r'[!@#$%^&*(),.?":{}|<>]').search(nickname):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=NicknameValidationResponse(
                is_valid=False, message="Nicknames cannot contain special characters"
            ).model_dump(),
        )
    try:
        User.get(User.nickname == nickname)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=NicknameValidationResponse(
                is_valid=False, message="Nickname already exists"
            ).model_dump(),
        )
    except DoesNotExist:
        return NicknameValidationResponse(is_valid=True)


@router.put(
    "/{user_id}/nickname",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=UserResponse,
    description=UPDATE_USER_NICKNAME_DESC,
)
async def update_user_nickname(
        request: Request, user_id: int, form: UserNicknameUpdateRequest
):
    login_user = User.get_by_id(request.state.token_info["id"])
    nickname = form.model_dump()["nickname"]
    if login_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    login_user.nickname = nickname
    login_user.save()
    return UserResponse.from_orm(login_user)


@router.put(
    "/{user_id}/image",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=UserResponse,
    description=UPDATE_USER_IMAGE_DESC,
)
async def update_user_image(request: Request, user_id: int, image_url: str):
    login_user: User = User.get_by_id(request.state.token_info["id"])
    if login_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    login_user.update(image=image_url)
    login_user.image = image_url

    return UserResponse.from_orm(login_user)


@router.put(
    "/{user_id}/preference",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=UserResponse,
    description=UPDATE_USER_PREFERENCE_DESC,
)
async def update_user_preference(
        request: Request, user_id: int, form: UserPreferenceUpdateRequest
):
    login_user = User.get_by_id(request.state.token_info["id"])
    preference = form.model_dump()
    if login_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    login_user.preference = preference
    login_user.save()
    return UserResponse.from_orm(login_user)


@router.delete(
    "/{user_id}", dependencies=[Depends(transactional), Depends(AuthRequired())]
)
async def delete_user(request: Request, user_id: int):
    login_user: User = User.get_by_id(request.state.token_info["id"])
    if login_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    login_user.uid = f"DELETED-{login_user.uid}+{time.time()}"
    login_user.is_deleted = True
    (
        FeedLike.update(is_deleted=True)
        .where(FeedLike.user_id == login_user.id)
        .execute()
    )
    (Feed.update(is_deleted=True).where(Feed.user_id == login_user.id).execute())
    (Comment.update(is_deleted=True).where(Comment.user_id == login_user.id).execute())
    login_user.save()

    return {"result": True}


@router.post(
    "/{target_user_id}/block",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=UserBlockResponse,
)
async def block_user(request: Request, target_user_id: int):
    login_user: User = User.get_or_raise(request.state.token_info["id"])
    already_blocked_user = UserBlock.get_or_none(
        UserBlock.user == login_user.id, UserBlock.blocked_user == target_user_id
    )

    if already_blocked_user is not None:
        (
            UserBlock.update(is_deleted=False)
            .where(
                UserBlock.user == login_user.id,
                UserBlock.blocked_user == target_user_id,
            )
            .execute()
        )
        return UserBlockResponse(target_user_id=target_user_id)

    UserBlock.create(user_id=login_user.id, blocked_user_id=target_user_id)

    return UserBlockResponse(target_user_id=target_user_id)


@router.delete(
    "/{target_user_id}/block",
    dependencies=[Depends(transactional), Depends(AuthRequired())],
    response_model=UserBlockResponse,
)
async def block_user(request: Request, target_user_id: int):
    login_user: User = User.get_or_raise(request.state.token_info["id"])
    (
        UserBlock.update(is_deleted=True)
        .where(
            UserBlock.user == login_user.id, UserBlock.blocked_user == target_user_id
        )
        .execute()
    )

    return UserBlockResponse(target_user_id=target_user_id)
