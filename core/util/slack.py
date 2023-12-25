import json
import os

import requests

from core.config.var_config import IS_PROD

if IS_PROD:
    webhook_rul = os.environ.get("SLACK_WEB_HOOK_URL")
else:
    from core.config import secrets

    webhook_rul = secrets.SLACK_WEB_HOOK_URL


async def send_slack_message(
    sender_name: str, channel: str, icon_emoji: str, message: str
):
    requests.post(
        webhook_rul,
        data=json.dumps(
            {
                "username": sender_name,
                "channel": channel,
                "icon_emoji": icon_emoji,
                "text": message,
            }
        ),
    )
