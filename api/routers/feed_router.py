from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.config.orm_config import transactional
from core.domain.feed_model import Feed
from core.dto.feed_dto import FeedResponse, FeedUpdateRequest

router = APIRouter(
    prefix="/feed",
    tags=["Feed"],
)


@router.get(
    "/{feed_id}",
    dependencies=[Depends(transactional)],
    response_model=FeedResponse,
)
async def get_feed_by_id(request: Request, feed_id: int):
    feed = Feed.get_by_id(feed_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=FeedResponse.from_orm(feed).model_dump()
    )


@router.put(
    "/{feed_id}",
    dependencies=[Depends(transactional)],
    response_model=FeedResponse,
)
async def update_feed(request: Request, feed_id: int, request_body: FeedUpdateRequest):
    feed = Feed.get_by_id(feed_id)
    feed.content = request_body.content
    feed.save()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=FeedResponse.from_orm(feed).model_dump()
    )
