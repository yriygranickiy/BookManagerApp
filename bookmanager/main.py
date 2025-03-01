import uvicorn
from fastapi import FastAPI
from app_bookmanager.controllers.book_manager_controller import router as book_manager_router
from app_bookmanager.controllers.author_manager_controller import router as author_manager_router
from app_bookmanager.controllers.book_instance_manager_controller import router as book_instance_manager_router
from app_bookmanager.controllers.genre_manager_controller import router as genre_manager_router
from app_bookmanager.controllers.publisher_manager_controller import router as publisher_manager_router


app_book_manager = FastAPI()

app_book_manager.include_router(book_manager_router)
app_book_manager.include_router(author_manager_router)
app_book_manager.include_router(book_instance_manager_router)
app_book_manager.include_router(genre_manager_router)
app_book_manager.include_router(publisher_manager_router)


if __name__ == '__main__':
    uvicorn.run(app_book_manager, host='0.0.0.0', port=8001)