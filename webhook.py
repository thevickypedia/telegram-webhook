import requests
from pydantic import HttpUrl
from config import settings, logger

session = requests.Session()


def get_webhook():
    get_info = f"https://api.telegram.org/bot{settings.bot_token}/getWebhookInfo"
    response = session.get(url=get_info)
    if response.ok:
        logger.info(response.json())
        return response.json()
    response.raise_for_status()


def delete_webhook():
    del_info = f"https://api.telegram.org/bot{settings.bot_token}/setWebhook?url="
    response = session.post(url=del_info)
    if response.ok:
        logger.info("Webhook has been cleared")
        return response.json()
    response.raise_for_status()


def set_webhook(webhook: HttpUrl):
    put_info = f"https://api.telegram.org/bot{settings.bot_token}/setWebhook?url={webhook}"
    response = session.post(url=put_info)
    if response.ok:
        logger.info("Webhook has been set to: %s", webhook)
        return response.json()
    response.raise_for_status()
