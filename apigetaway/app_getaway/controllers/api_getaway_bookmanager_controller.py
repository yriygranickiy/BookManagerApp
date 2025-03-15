import json
import os
import uuid
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException

from app_getaway.decorators.decorator import require_permission
from app_getaway.schema.book_schema import BookInstanceRequest, BookRequest, GenreToBookRequest, PublisherToBookRequest, \
    AuthorToBookRequest, GenreRequest, PublisherRequest
from app_getaway.security.auth import get_user_meta

router = APIRouter(prefix="/apigetaway", tags=["apigetaway_bookmanager"])


IN_DOCKER = os.path.exists("/.dockerenv")
MICROSERVICE_BOOKMANAGER_URL = "http://book-manager-service:8001" if IN_DOCKER else "http://localhost:8001"


#BOOK_ENDPOINST
@router.post('book/create-book')
@require_permission(["CREATE_BOOK"])
def forward_create_book(meta: Annotated[dict, Depends(get_user_meta)],
                        data: BookRequest):
    try:
        payload = data.model_dump_json()
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not payload:
            raise HTTPException(status_code=400,detail="Empty payload")
        response = requests.post(f'{MICROSERVICE_BOOKMANAGER_URL}/',
                                 json=payload,
                                 headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Book not created!")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book service error: {str(e)}')

@router.post('book/add-genre-to-book')
@require_permission(["CREATE_BOOK"])
def forward_add_genre_to_book(meta: Annotated[dict, Depends(get_user_meta)],
                              data:GenreToBookRequest):
    try:
        payload = data.model_dump_json()
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not payload:
            raise HTTPException(status_code=400,detail="Empty payload")
        response = requests.post(f'{MICROSERVICE_BOOKMANAGER_URL}/book/add-genre-to-book',
                                 json=payload,
                                 headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Genre to book not added!")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book service error: {str(e)}')
@router.post('book/add-publisher-to-book')
@require_permission(["CREATE_BOOK"])
def forward_add_publisher_to_book(meta: Annotated[dict, Depends(get_user_meta)],
                                  data: PublisherToBookRequest):
    try:
        payload = data.model_dump_json()
        headers={
            "permissions": f'{meta["permissions"]}'
        }
        if not payload:
            raise HTTPException(status_code=400,detail="Empty payload")
        response = requests.post(f'{MICROSERVICE_BOOKMANAGER_URL}/book/add-publisher-to-book',
                                 json=payload,
                                 headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Publisher to book not added!")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book service error: {str(e)}')

@router.post('book/add-author-to-book')
@require_permission(["CREATE_BOOK"])
def forward_add_author_to_book(meta: Annotated[dict, Depends(get_user_meta)],
                               data: AuthorToBookRequest):
    try:
        payload = data.model_dump_json()
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not payload:
            raise HTTPException(status_code=400,detail="Empty payload")
        response = requests.post(f'{MICROSERVICE_BOOKMANAGER_URL}/book/add-author-to-book',
                                 json=payload,
                                 headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Author to book not added!")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book service error: {str(e)}')

@router.put('book/update-book/{id}')
@require_permission(["UPDATE_BOOK"])
def forward_update_book(meta: Annotated[dict, Depends(get_user_meta)],
                        id: uuid.UUID, updated_book:dict):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not updated_book:
            raise HTTPException(status_code=400,detail="Empty payload")
        response = requests.put(f'{MICROSERVICE_BOOKMANAGER_URL}/update-book/{id}',
                                json=json.dumps(updated_book),
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Book not updated!")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book service error: {str(e)}')

@router.get('book/get-book/{id}')
@require_permission(["GET_BOOK"])
def forward_get_book_by_id(meta: Annotated[dict, Depends(get_user_meta)],
                           id: uuid.UUID):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/book/get-book/{id}',
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Book with id : {id}  not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book service error: {str(e)}')

@router.get('/book/get-books')
@require_permission(["READ_BOOK"])
def forward_get_all_books(meta: Annotated[dict, Depends(get_user_meta)]):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/book/get-books', headers=headers)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')

@router.get('/book/get-authors-from-book/{title}')
@require_permission(["READ_BOOK"])
def forward_get_authors_from_book_by_title(meta: Annotated[dict, Depends(get_user_meta)],
                                           title: str):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not title:
            raise HTTPException(status_code=400,detail="Empty title")
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/book/get-authors-from-book/{title}',
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Books with title: {title} not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book service error: {str(e)}')

@router.delete('/book/delete-book/{id}')
@require_permission(["DELETE_BOOK"])
def forward_delete_book(meta: Annotated[dict, Depends(get_user_meta)],
                        id: uuid.UUID):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.delete(f'{MICROSERVICE_BOOKMANAGER_URL}/book/remove-book/{id}',
                                   headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Book with id : {id}  not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book service error: {str(e)}')


#BOOK_INSTANCE_ENDPOINTS
@router.post('/create-book-instance')
@require_permission(["CREATE_BOOK_INSTANCE"])
def forward_create_book_instance(meta: Annotated[dict, Depends(get_user_meta)],
                                             data: BookInstanceRequest):
    try:
        payload = data.model_dump_json()
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        headers = {
            "permissions": f'{meta["permissions"]}'
        }

        response = requests.post(f'{MICROSERVICE_BOOKMANAGER_URL}/book_instance/create-book-instance', headers=headers,
                                 data=payload)

        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')

@router.put('/update-book-instance/{id}')
@require_permission(["UPDATE_BOOK_INSTANCE"])
def forward_update_book_instance(meta: Annotated[dict, Depends(get_user_meta)],
                                              id: uuid.UUID, updated_data: dict):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}',
            "username": meta["username"]
        }
        response = requests.put(f'{MICROSERVICE_BOOKMANAGER_URL}/book_instance/update-book-instance/{id}',
                                headers=headers,
                                data=json.dumps(updated_data))
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')

@router.get('/book_instance/get-all')
@require_permission(["READ_BOOK_INSTANCE"])
def forward_get_all_book_instances(meta: Annotated[dict, Depends(get_user_meta)]):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/book_instance/get-all',
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Book instances not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book instance service error: {str(e)}')

@router.get('/book_instance/{id}')
@require_permission(["READ_BOOK_INSTANCE"])
def forward_get_book_by_id(meta: Annotated[dict, Depends(get_user_meta)],
                           id: uuid.UUID):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/book_instance/{id}',
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Book instance with id: {id} not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book instance service error: {str(e)}')

@router.delete('/book_instance/{id}')
@require_permission(["DELETE_BOOK_INSTANCE"])
def forward_delete_book_instance_by_id(meta: Annotated[dict, Depends(get_user_meta)],
                                       id: uuid.UUID):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.delete(f'{MICROSERVICE_BOOKMANAGER_URL}/book_instance/{id}',
                                   headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Book instance with id: {id} not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Book instance service error: {str(e)}')

#GENRE_CONTROLLER
@router.post('/genre/create-genre')
@require_permission(["CREATE_GENRE"])
def forward_create_genre(meta: Annotated[dict, Depends(get_user_meta)],
                         data: GenreRequest):
    try:
        payload = data.model_dump_json()
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        response = requests.post(f'{MICROSERVICE_BOOKMANAGER_URL}/genre/create-genre',
                                 headers=headers,
                                 data=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Genre creation failed')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Genre creation service error: {str(e)}')

@router.put('/genre/update-genre/{id}')
@require_permission(["UPDATE_GENRE"])
def forward_update_genre(meta: Annotated[dict, Depends(get_user_meta)],
                         id: uuid.UUID, updated_data: dict):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.put(f'{MICROSERVICE_BOOKMANAGER_URL}/genre/update-genre/{id}',
                                headers=headers,
                                data=json.dumps(updated_data))
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Genre with id: {id} update failed')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Genre service error: {str(e)}')

@router.get('/genre/get-all')
@require_permission(["READ_GENRE"])
def forward_get_all_genres(meta: Annotated[dict, Depends(get_user_meta)]):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/genre/get-all', headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Genres not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Genres service error: {str(e)}')

@router.get('/genre/{id}')
@require_permission(["READ_GENRE"])
def forward_get_genre_by_id(meta: Annotated[dict, Depends(get_user_meta)],
                            id: uuid.UUID):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/genre/{id}', headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Genre with id: {id} not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Genre service error: {str(e)}')

@router.get('/genre/get-books-by-title/{title}')
@require_permission(["READ_GENRE"])
def forward_get_books_by_genre(meta: Annotated[dict, Depends(get_user_meta)],
                               title:str):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not title:
            raise HTTPException(status_code=400,detail="Empty title")
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/genre/get-books-by-title/{title}',
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Books by genre title : {title} not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Genre service error: {str(e)}')

@router.delete('/genre/delete-genre/{id}')
@require_permission(["DELETE_GENRE"])
def forward_delete_genre_by_id(meta: Annotated[dict, Depends(get_user_meta)],
                               id: uuid.UUID):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.delete(f'{MICROSERVICE_BOOKMANAGER_URL}/genre/{id}', headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Genre with id: {id} not found!')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Genre service error: {str(e)}')

#PUBLISHER_CONTROLLER

@router.post('/publisher/create-publisher')
@require_permission(["CREATE_PUBLISHER"])
def forward_create_publisher(meta: Annotated[dict, Depends(get_user_meta)],
                             data: PublisherRequest):
    try:
        payload = data.model_dump_json()
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not data:
            raise HTTPException(status_code=400,detail="Empty data")
        response = requests.post(f'{MICROSERVICE_BOOKMANAGER_URL}/publisher/create-publisher',
                                 headers=headers,
                                 data=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Publisher creation failed')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Publisher service error: {str(e)}')

@router.put('/publisher/update-publisher/{id}')
@require_permission(["UPDATE_PUBLISHER"])
def forward_update_publisher(meta: Annotated[dict, Depends(get_user_meta)],
                             id:uuid.UUID,
                             update_data: dict):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }

        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.put(f'{MICROSERVICE_BOOKMANAGER_URL}/publisher/update-publisher/{id}',
                                headers=headers,
                                data=json.dumps(update_data))
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Publisher update failed')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Publisher service error: {str(e)}')

@router.get('/publisher/get-all')
@require_permission(["READ_PUBLISHER"])
def forward_get_all_publisher(meta: Annotated[dict, Depends(get_user_meta)]):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/publisher/get-all',
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Publisher get all failed')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Publisher service error: {str(e)}')

@router.get('/publisher/{id}')
@require_permission(["READ_PUBLISHER"])
def forward_get_publisher_by_id(meta: Annotated[dict, Depends(get_user_meta)],
                                id:uuid.UUID):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/publisher/{id}',
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Publisher get publisher {id} failed')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Publisher service error: {str(e)}')

@router.get('/publisher/get-books-from-publisher/{title}')
def forward_get_books_from_publisher_by_title(meta: Annotated[dict, Depends(get_user_meta)],
                                              title:str):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not title:
            raise HTTPException(status_code=400,detail="Empty title")
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/publisher/get-books-from-publisher/{title}',
                                headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Publisher get books from publisher {title} failed')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Publisher service error: {str(e)}')

@router.delete('/publisher/{id}')
def forward_delete_publisher(meta: Annotated[dict, Depends(get_user_meta)],
                             id:uuid.UUID):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        if not id:
            raise HTTPException(status_code=400,detail="Empty id")
        response = requests.delete(f'{MICROSERVICE_BOOKMANAGER_URL}/publisher/{id}',
                                   headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f'Publisher delete failed')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Publisher service error: {str(e)}')

