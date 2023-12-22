import json

import requests

from core.config.secrets import SLACK_WEB_HOOK_URL


async def send_slack_message(message: str):
    requests.post(SLACK_WEB_HOOK_URL, data=json.dumps({"text": message}))
