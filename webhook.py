import requests
from config import settings

session = requests.Session()


def get_webhook():
    get_info = f"https://api.telegram.org/bot{settings.bot_token}/getWebhookInfo"
    response = session.get(url=get_info)
    print(response.json())


def delete_webhook():
    del_info = f"https://api.telegram.org/bot{settings.bot_token}/setWebhook?url="
    response = session.post(url=del_info)
    print(response.json())


def set_webhook():
    put_info = f"https://api.telegram.org/bot{settings.bot_token}/setWebhook?url={settings.webhook}"
    response = session.post(url=put_info)
    print(response.json())


if __name__ == '__main__':
    set_webhook()
    # delete_webhook()
    get_webhook()
