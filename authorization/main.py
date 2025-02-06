import uvicorn
from fastapi import FastAPI

from app_authorization.controllers.auth_controller import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["authorization"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)