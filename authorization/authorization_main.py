import uvicorn
from fastapi import FastAPI

from app_authorization.controllers.auth_controller import router as auth_router
from app_authorization.controllers.admin_controller import router as admin_router_role

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router_role)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

