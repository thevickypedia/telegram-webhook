import requests
from pydantic import HttpUrl

from config import settings, logger

BASE_URL = f"https://api.telegram.org/bot{settings.bot_token}"
SESSION = requests.Session()


def get_webhook():
    get_info = f"{BASE_URL}/getWebhookInfo"
    response = SESSION.get(url=get_info)
    if response.ok:
        logger.info(response.json())
        return response.json()
    response.raise_for_status()


def delete_webhook():
    del_info = f"{BASE_URL}/setWebhook"
    response = SESSION.post(url=del_info, params=dict(url=None))
    if response.ok:
        logger.info("Webhook has been removed.")
        return response.json()
    response.raise_for_status()


def set_webhook(webhook: HttpUrl):
    put_info = f"{BASE_URL}/setWebhook"
    response = SESSION.post(url=put_info, params=dict(url=webhook))
    if response.ok:
        logger.info("Webhook has been set to: %s", webhook)
        return response.json()
    response.raise_for_status()
