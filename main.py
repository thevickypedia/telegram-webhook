import uvicorn
from fastapi import FastAPI

from config import settings
from routes import router
from tunnel import Tunnel

with open('README.md') as file:
    long_description = '\n'.join(file.readlines()[1:]).strip()

app = FastAPI(
    title="Telegram API Webhook",
    description=long_description,
)
app.include_router(router)

if __name__ == '__main__':
    tunnel = Tunnel()
    uvicorn.run(host=settings.host, port=settings.port, app=app)
