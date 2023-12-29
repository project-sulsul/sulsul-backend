from enum import Enum
from typing import Optional

from pydantic import BaseModel
from fastapi_events.registry.payload_schema import registry as payload_schema


class CommentEvents(Enum):
    CREATE_COMMENT = "CREATE_COMMENT"


@payload_schema.register(event_name=CommentEvents.CREATE_COMMENT)
class CreateCommentPayload(BaseModel):
    feed_owner_user_id: int
    parent_comment_writer_user_id: Optional[int] = None
    comment_writer_user_id: int
    comment_id: int  # 지금 생성 완료된 댓글 id
