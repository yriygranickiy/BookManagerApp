import uvicorn
from fastapi import FastAPI
from bookmanager.app.controllers.book_manager_controller import router as book_manager_router
from bookmanager.app.controllers.author_manager_controller import router as author_manager_router

app_book_manager = FastAPI()

app_book_manager.include_router(book_manager_router)
app_book_manager.include_router(author_manager_router)


if __name__ == '__main__':
    uvicorn.run(app_book_manager, host='127.0.0.1', port=8001)