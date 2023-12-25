import json

import requests

from core.config.secrets import SLACK_WEB_HOOK_URL


async def send_slack_message(
    sender_name: str, channel: str, icon_emoji: str, message: str
):
    requests.post(
        SLACK_WEB_HOOK_URL,
        data=json.dumps(
            {
                "username": sender_name,
                "channel": channel,
                "icon_emoji": icon_emoji,
                "text": message,
            }
        ),
    )
