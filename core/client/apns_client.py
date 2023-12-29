from enum import Enum
from typing import Optional, List

from aioapns import APNs, NotificationRequest, PushType
from pydantic import BaseModel

from core.util.logger import logger


class DeviceType(Enum):
    IOS = "IOS"
    ANDROID = "ANDROID"


class PushRequest(BaseModel):
    device_token: str
    device_type: DeviceType
    title: str
    content: str
    is_sendable: bool = False  # 알림 수신 여부
    target_type: Optional[str] = None
    target_id: Optional[int] = None


class PushClient:
    async def send_push(self, request: PushRequest):
        pass

    async def send_push_batch(self, requests: List[PushRequest]):
        pass


class PushClientImpl(PushClient):
    def __init__(
        self,
        ios_client: Optional[PushClient] = None,
        android_client: Optional[PushClient] = None,
    ):
        self.ios_client = ios_client
        self.android_client = android_client

    async def send_push(self, request: PushRequest):
        if request.is_sendable is False:
            return
        if request.device_type == DeviceType.IOS:
            await self.ios_client.send_push(request)
        elif request.device_type == DeviceType.ANDROID:
            await self.android_client.send_push(request)

    async def send_push_batch(self, requests: List[PushRequest]):
        pass


class APNSClient(PushClient):
    def __init__(
        self,
        apns_key_path: str,
        key_id: str,
        team_id: str,
        topic: str,
        use_sandbox: bool,
    ):
        self.apns_key_client = APNs(
            key=apns_key_path,
            key_id=key_id,
            team_id=team_id,
            topic=topic,  # Bundle ID
            use_sandbox=use_sandbox,
        )

    async def send_push(self, request: PushRequest):
        apns_request = NotificationRequest(
            device_token=request.device_token,
            message={
                "aps": {
                    "alert": {
                        "title": request.title,
                        "body": request.content,
                    },
                    "target_type": request.target_type,
                    "target_id": request.target_id,
                }
            },
            push_type=PushType.ALERT,
        )

        try:
            await self.apns_key_client.send_notification(apns_request)
        except Exception:
            logger.error(f"Failed to send push to :: {request}")
            pass

    async def send_push_batch(self, requests: List[PushRequest]):
        # TODO: implement
        pass


# ios_push_client = APNSClient(
#     apns_key_path="/Users/jeonghun/Documents/Projects/Python/boilerplate/ios_push_key.p8",
#     key_id="",
#     team_id="",
#     topic="",
#     use_sandbox=False
# )
ios_push_client = None
android_push_client = None  # TODO: implement

push_client = PushClientImpl(
    ios_client=ios_push_client, android_client=android_push_client
)
