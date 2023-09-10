import httpx
import uvicorn
from fastapi import APIRouter, Request, FastAPI

from config import settings

router = APIRouter()
app = FastAPI(
    title="TelegramAPI",
)
BASE_URL = f"https://api.telegram.org/bot{settings.bot_token}"
client = httpx.AsyncClient()


@app.post("/")
async def webhook(req: Request):
    data = await req.json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    await client.post(f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={text}")


if __name__ == '__main__':
    uvicorn.run(host="localhost", port=8443, app=app)
