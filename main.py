from threading import Thread

import httpx
import uvicorn
from fastapi import APIRouter, Request, FastAPI

from config import settings, logger
from tunnel import ngrok_connection
from webhook import set_webhook

router = APIRouter()
app = FastAPI(docs_url=None, redoc_url=None)
client = httpx.AsyncClient()


@app.post("/")
async def webhook_check(req: Request):
    response = await req.json()
    chat_id = response['message']['chat']['id']
    text = response['message']['text']
    # send the same message back to the user
    await client.post(f"https://api.telegram.org/bot{settings.bot_token}/sendMessage?chat_id={chat_id}&text={text}")


if __name__ == '__main__':
    if public_url := ngrok_connection():
        logger.info("http://%s:%s -> %s", settings.host, settings.port, public_url)
        Thread(target=set_webhook, args=(public_url,)).start()
    else:
        raise RuntimeError("Failed to fetch webhook, cannot initiate tunneling.")
    uvicorn.run(host=settings.host, port=settings.port, app=app)
