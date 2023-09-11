import os
from threading import Thread

import httpx
import uvicorn
from fastapi import APIRouter, Request, FastAPI

from config import settings, logger
from tunnel import ngrok_connection, Tunnel
from webhook import set_webhook

router = APIRouter()
app = FastAPI(docs_url=None, redoc_url=None)
client = httpx.AsyncClient()


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down webhook server")
    tunnel.kill()
    os._exit(0)  # noqa


@app.post("/")
async def webhook_check(req: Request):
    response = await req.json()
    chat_id = response['message']['chat']['id']
    text = response['message']['text']
    if 'stop' in text or 'exit' in text or 'kill' in text:
        text = "Stopping webhook server and ngrok tunnel"
        os.kill(os.getpid(), 15)  # Send a terminate signal for the current process ID triggering shutdown event
    await client.post(
        url=f"https://api.telegram.org/bot{settings.bot_token}/sendMessage",
        params={'chat_id': chat_id, 'text': text}
    )


if __name__ == '__main__':
    if public_url := ngrok_connection():
        logger.info("http://%s:%s -> %s", settings.host, settings.port, public_url)
        Thread(target=set_webhook, args=(public_url,)).start()
        tunnel = Tunnel()
        tunnel.start()
    else:
        raise RuntimeError("Failed to fetch webhook, cannot initiate tunneling.")
    uvicorn.run(host=settings.host, port=settings.port, app=app)
