import os
from http import HTTPStatus
from json.decoder import JSONDecodeError
from threading import Thread
from urllib.parse import urljoin

import httpx
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from config import settings, logger
from tunnel import Tunnel, ngrok_connection
from webhook import set_webhook, delete_webhook

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
    if public_url:
        logger.info("http://%s:%s -> %s", settings.host, settings.port, public_url)
        Thread(target=set_webhook, args=(urljoin(public_url, settings.endpoint),)).start()
        tunnel.start()
    else:
        raise RuntimeError("Failed to fetch webhook, cannot initiate tunneling.")


@router.on_event("shutdown")
async def shutdown():
    tunnel.kill()
    delete_webhook()
    os._exit(0)  # noqa


@router.post(settings.endpoint)
async def telegram_webhook(request: Request):
    """Invoked when a new message is received from Telegram API.

    Args:
        request: Request instance.

    Raises:

        HTTPException:
            - 406: If the request payload is not JSON format-able.
    """
    try:
        response = await request.json()
    except JSONDecodeError as error:
        logger.error(error)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.real, detail=HTTPStatus.BAD_REQUEST.phrase)
    chat_id = None
    try:
        chat_id = response['message']['chat']['id']
        text = response['message']['text']
    except KeyError as error:
        if chat_id:
            logger.info(response)
            text = "Currently supports only text"
        else:
            logger.error(error)
            raise HTTPException(status_code=HTTPStatus.NOT_ACCEPTABLE.real, detail=HTTPStatus.NOT_ACCEPTABLE.phrase)
    if 'stop' in text or 'exit' in text or 'kill' in text:
        text = "Stopping webhook server and ngrok tunnel"
        os.kill(os.getpid(), 15)  # Send a terminate signal for the current process ID triggering shutdown event
    await client.post(
        url=f"https://api.telegram.org/bot{settings.bot_token}/sendMessage",
        params={'chat_id': chat_id, 'text': text}
    )
