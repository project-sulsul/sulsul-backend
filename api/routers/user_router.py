from fastapi import APIRouter, Depends, Request, UploadFile, status, HTTPException
from fastapi.responses import JSONResponse

import re
import uuid
from peewee import DoesNotExist

from api.config.middleware import auth, auth_required
from core.config.orm_config import transactional
from core.client.nickname_generator_client import NicknameGeneratorClient
from core.client.aws_client import S3Client
from core.domain.user_model import User
from core.dto.user_dto import UserResponse
from core.dto.user_dto import UserNicknameUpdateRequest
from core.dto.user_dto import UserPreferenceUpdateRequest
from core.dto.user_dto import NicknameResponse
from core.dto.user_dto import NicknameValidationResponse
from core.config.var_config import USER_NICKNAME_MAX_LENGTH

from api.descriptions.user_api_descriptions import *

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get(
    "/nickname",
    dependencies=[Depends(transactional)],
    response_model=NicknameResponse,
    description=GENERATE_RANDOM_NICKNAME_DESC,
)
@auth_required
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
    dependencies=[Depends(transactional)],
    response_model=UserResponse,
    description=GET_USER_BY_ID_DESC,
)
@auth
async def get_user_by_id(request: Request, user_id: int):
    user = User.get_or_none(User.id == user_id, User.is_deleted == False)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"User {user_id} doesn't exist"},
        )
    return UserResponse.from_orm(user)


@router.get(
    "/validation",
    dependencies=[Depends(transactional)],
    response_model=NicknameValidationResponse,
    description=VALIDATE_USER_NICKNAME_DESC,
)
@auth_required
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
    dependencies=[Depends(transactional)],
    response_model=UserResponse,
    description=UPDATE_USER_NICKNAME_DESC,
)
@auth_required
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
    dependencies=[Depends(transactional)],
    response_model=UserResponse,
    description=UPDATE_USER_IMAGE_DESC,
)
@auth_required
async def update_user_image(request: Request, user_id: int, file: UploadFile):
    login_user = User.get_by_id(request.state.token_info["id"])
    if login_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if file.size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file"
        )

    s3 = S3Client()
    key = f"profile_images/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    try:
        if login_user.image:
            s3.delete_object(f"profile_images/{login_user.image.split('/')[-1]}")
        s3.upload_fileobj(file.file, key)
        login_user.image = s3.get_object_url(key)
        login_user.save()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return UserResponse.from_orm(login_user)


@router.put(
    "/{user_id}/preference",
    dependencies=[Depends(transactional)],
    response_model=UserResponse,
    description=UPDATE_USER_PREFERENCE_DESC,
)
@auth_required
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


@router.delete("/{user_id}", dependencies=[Depends(transactional)])
@auth_required
async def delete_user(request: Request, user_id: int):
    login_user = User.get_by_id(request.state.token_info["id"])
    if login_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    login_user.is_deleted = True
    login_user.save()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": True})
