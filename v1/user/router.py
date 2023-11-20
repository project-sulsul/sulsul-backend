from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

import re
import requests
from peewee import DoesNotExist

from src.middleware import auth, auth_required
from src.orm import transactional
from v1.user.model import User
from v1.user.model import UserResponseModel
from v1.user.model import UserNicknameUpdateModel
from v1.user.model import UserPreferenceUpdateModel
from v1.user.model import NicknameResponseModel
from v1.user.model import NicknameValidationResponseModel
from src.config.var_config import USER_NICKNAME_MAX_LENGTH


router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get("/nickname", dependencies=[Depends(transactional)], response_model=NicknameResponseModel)
@auth_required
async def generate_random_nickname(request: Request):
    error_count = 0
    while error_count < 5:
        response = requests.get("https://nickname.hwanmoo.kr?format=json&count=20")
        if response.status_code != 200:
            error_count += 1
            continue

        nicknames = response.json()["words"]
        for nickname in nicknames:
            count = User.select().where(User.nickname == nickname).count()
            if count == 0 and not re.compile(r'[!@#$%^&*(),.?":{}|<>]').search(nickname) and len(nickname) <= USER_NICKNAME_MAX_LENGTH:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=NicknameResponseModel(nickname=nickname).model_dump(),
                )


@router.get("/{user_id}", dependencies=[Depends(transactional)], response_model=UserResponseModel)
@auth
async def get_user_by_id(request: Request, user_id: int):
    user = User.get_or_none(User.id == user_id, User.is_deleted == False)
    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"User {user_id} doesn't exist"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.dto().model_dump())


@router.get("/validation", dependencies=[Depends(transactional)], response_model=NicknameValidationResponseModel)
@auth
async def validate_user_nickname(request: Request, nickname: str):
    if len(nickname) > USER_NICKNAME_MAX_LENGTH:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content=NicknameValidationResponseModel(is_valid=False, message=f"Max length({USER_NICKNAME_MAX_LENGTH}) exceeded").model_dump()
        )
    if re.compile(r'[!@#$%^&*(),.?":{}|<>]').search(nickname):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content=NicknameValidationResponseModel(is_valid=False, message="Nicknames cannot contain special characters").model_dump()
        )
    try:
        User.get(User.nickname == nickname)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content=NicknameValidationResponseModel(is_valid=False, message="Nickname already exists").model_dump()
        )
    except DoesNotExist:
        return JSONResponse(status_code=status.HTTP_200_OK, content=NicknameValidationResponseModel(is_valid=True).model_dump())


@router.post("/{user_id}/nickname", dependencies=[Depends(transactional)], response_model=UserResponseModel)
@auth_required
async def update_user_nickname(request: Request, user_id: int, form: UserNicknameUpdateModel):
    login_user = User.get_by_id(request.state.user["id"])
    nickname = form.model_dump()["nickname"]
    if login_user.id != user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Forbidden request"})
    login_user.nickname = nickname
    login_user.save()
    return JSONResponse(status_code=status.HTTP_200_OK, content=login_user.dto().model_dump())


@router.post("/{user_id}/preference", dependencies=[Depends(transactional)], response_model=UserResponseModel)
@auth_required
async def update_user_preference(request: Request, user_id: int, form: UserPreferenceUpdateModel):
    login_user = User.get_by_id(request.state.user["id"])
    preference = form.model_dump()["preference"]
    if login_user.id != user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Forbidden request"})
    login_user.preference = preference
    login_user.save()
    return JSONResponse(status_code=status.HTTP_200_OK, content=login_user.dto().model_dump())


@router.delete("/{user_id}", dependencies=[Depends(transactional)])
@auth_required
async def delete_user(request: Request, user_id: int):
    login_user = User.get_by_id(request.state.user["id"])
    if login_user.id != user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Forbidden request"})
    login_user.is_deleted = True
    login_user.save()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": True})
