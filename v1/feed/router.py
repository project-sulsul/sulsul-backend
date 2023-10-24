from fastapi import APIRouter


router = APIRouter(
    prefix="/feed",
    tags=["Authentication"],
)


@router.get("")
async def user_test(request):
    return {}
