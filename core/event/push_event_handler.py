from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from core.client.apns_client import push_client
from core.event.events import CommentEvents


@local_handler.register(event_name=CommentEvents.CREATE_COMMENT)
async def handle_create_comment_send_push_handler(
    event: Event,
):
    print("야-호! 이벤트 핸들링 성공-!")
    print(push_client)
    event_name, payload = event
    print(f"event_name: {event_name} handled")
