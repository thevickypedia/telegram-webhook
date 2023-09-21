import json

import requests
from pydantic import HttpUrl

from models.config import settings, logger

BASE_URL = f"https://api.telegram.org/bot{settings.bot_token}"
SESSION = requests.Session()


def get_webhook():
    """
    https://core.telegram.org/bots/api#getwebhookinfo
    """
    get_info = f"{BASE_URL}/getWebhookInfo"
    response = SESSION.get(url=get_info)
    if response.ok:
        logger.info(response.json())
        return response.json()
    response.raise_for_status()


def delete_webhook():
    """
    https://core.telegram.org/bots/api#deletewebhook
    """
    del_info = f"{BASE_URL}/setWebhook"
    response = SESSION.post(url=del_info, params=dict(url=None))
    if response.ok:
        logger.info("Webhook has been removed.")
        return response.json()
    response.raise_for_status()


def set_webhook(webhook: HttpUrl):
    """
    https://core.telegram.org/bots/api#setwebhook
    """
    put_info = f"{BASE_URL}/setWebhook"
    payload = dict(
        url=webhook,
        secret_token=settings.secret_token,
        drop_pending_updates=settings.drop_pending_updates,
        max_connections=settings.max_connections,
        allowed_updates=json.dumps(settings.allowed_updates)
    )
    if settings.webhook_ip:
        payload['ip_address'] = settings.webhook_ip.__str__()
    logger.debug(payload)
    if settings.certificate:
        response = SESSION.post(url=put_info, data=payload,
                                files={'certificate': (settings.certificate.stem + settings.certificate.suffix,
                                                       settings.certificate.open(mode="rb"))})
    else:
        response = SESSION.post(url=put_info, params=payload)
    if response.ok:
        logger.info("Webhook has been set to: %s", webhook)
        return response.json()
    response.raise_for_status()
