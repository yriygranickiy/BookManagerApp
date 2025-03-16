import uvicorn
from fastapi import FastAPI

from app_getaway.controllers.api_getaway_auth_controller  import router as api_getaway_auth
from app_getaway.controllers.api_getaway_bookmanager_controller import router as api_getaway_bookmanager
app_api_getaway = FastAPI()

app_api_getaway.include_router(api_getaway_auth)
app_api_getaway.include_router(api_getaway_bookmanager)


if __name__ == '__main__':
    uvicorn.run(app_api_getaway, host="0.0.0.0", port=8080)
