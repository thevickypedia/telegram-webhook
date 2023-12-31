import uvicorn
from fastapi import FastAPI

from models.config import settings
from models.routes import router

with open('README.md') as file:
    readme_data = file.readlines()

app = FastAPI(
    title=readme_data[0].lstrip('#'),
    description='\n'.join(readme_data[1:]).strip(),
)
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(host=settings.host, port=settings.port.real, app=app)
