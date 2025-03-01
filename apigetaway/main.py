import uvicorn
from fastapi import FastAPI

from app_getaway.controllers.api_getaway_controller import router as api_getaway_router

#TODO: закрыть доступ к сервисам и дать доступ только через API GEATAWAY

app_api_getaway = FastAPI()

app_api_getaway.include_router(api_getaway_router)


if __name__ == '__main__':
    uvicorn.run(app_api_getaway, host="0.0.0.0", port=8080)
