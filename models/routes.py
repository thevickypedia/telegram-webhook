import os
import secrets
from http import HTTPStatus
from json.decoder import JSONDecodeError
from threading import Thread
from urllib.parse import urljoin

import httpx
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from models.config import settings, logger
from models.processor import serialize
from models.tunnel import Tunnel, ngrok_connection
from models.webhook import set_webhook, delete_webhook

client = httpx.AsyncClient()
router = APIRouter()
tunnel = Tunnel()


@router.get(path="/", response_class=RedirectResponse, include_in_schema=False)
async def redirect_index():
    """Redirect to docs in read-only mode.

    Returns:

        str:
        Redirects the root endpoint / url to read-only doc location.
    """
    return "/redoc"


@router.on_event("startup")
async def startup() -> None:
    if settings.webhook:
        public_url = str(settings.webhook)
    else:
        public_url = ngrok_connection()
        tunnel.start()  # starts regardless of ngrok connection as it is killed before raising runtime error
    if public_url:
        logger.info("http://%s:%s -> %s", settings.host, settings.port.real, public_url)
        Thread(target=set_webhook, args=(urljoin(public_url, settings.endpoint),)).start()
    else:
        if tunnel.is_alive():
            tunnel.kill()
        raise RuntimeError("\n\nFailed to fetch webhook, cannot initiate tunneling.")


@router.on_event("shutdown")
async def shutdown():
    if settings.ngrok_token:
        tunnel.kill()
    delete_webhook()
    os._exit(0)  # noqa


def two_factor(request: Request):
    if settings.secret_token:  # only validates if secret_token env var is set
        if secrets.compare_digest(request.headers.get('X-Telegram-Bot-Api-Secret-Token', ''), settings.secret_token):
            return True
    else:
        return True


@router.post(settings.endpoint)
async def telegram_webhook(request: Request):
    """Invoked when a new message is received from Telegram API.

    Args:
        request: Request instance.

    Raises:

        HTTPException:
            - 406: If the request payload is not JSON format-able.
    """
    logger.debug("Connection received from %s via %s", request.client.host, request.headers.get('host'))
    try:
        response = await request.json()
    except JSONDecodeError as error:
        logger.error(error)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.real, detail=HTTPStatus.BAD_REQUEST.phrase)
    # Ensure only the owner who set the webhook can interact with the Bot
    if not two_factor(request):
        logger.error("Request received from a non-webhook source")
        logger.error(response)
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN.real, detail=HTTPStatus.FORBIDDEN.phrase)
    response, chat_id = serialize(response['message'])
    await client.post(
        url=f"https://api.telegram.org/bot{settings.bot_token}/sendMessage",
        params={'chat_id': chat_id, 'text': response}
    )
