import json
import os
import uuid
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException

from app_getaway.decorators.decorator import require_permission
from app_getaway.schema.schema import BookInstanceRequest
from app_getaway.security.auth import get_user_meta

router = APIRouter(prefix="/apigetaway", tags=["apigetaway_bookmanager"])


IN_DOCKER = os.path.exists("/.dockerenv")
MICROSERVICE_BOOKMANAGER_URL = "http://book-manager-service:8001" if IN_DOCKER else "http://localhost:8001"


#BOOK_ENDPOINST
@router.get('/book/get-books')
@require_permission(["READ_BOOK"])
def forward_bookmanager_request(meta: Annotated[dict, Depends(get_user_meta)]):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}'
        }
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/book/get-books', headers=headers)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')


#BOOK_INSTANCE_ENDPOINTS
@router.post('/create-book-instance')
@require_permission(["CREATE_BOOK_INSTANCE"])
def forward_bookmanager_book_instance_create(meta: Annotated[dict, Depends(get_user_meta)],
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
def forward_bookmanager_book_instance_request(meta: Annotated[dict, Depends(get_user_meta)],
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
