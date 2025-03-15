import http.client
import json
import uuid
from typing import Annotated

import os
import requests
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException
from kafka import KafkaProducer

from app_getaway.decorators.decorator import require_permission
from app_getaway.schema.schema import LoginRequest, BookInstanceRequest
from app_getaway.security.auth import get_user_meta

router = APIRouter(prefix='/apigetaway', tags=['apigetaway'])

IN_DOCKER = os.path.exists("/.dockerenv")
MICROSERVICE_AUTH_URL = "http://app-auth-service:8000/auth" if IN_DOCKER else "http://localhost:8000/auth"
MICROSERVICE_BOOKMANAGER_URL = "http://book-manager-service:8001" if IN_DOCKER else "http://localhost:8001"

load_dotenv()

@router.post('/auth/login')
def forward_auth_request(data: LoginRequest):
    try:
        payload = data.model_dump_json()
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(f'{MICROSERVICE_AUTH_URL}/login', headers=headers, data=payload)

        return response.json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')


@router.get('/auth/get-all-users')
@require_permission(["READ_USER"])
def forward_auth_request_get_all_users(meta: Annotated[dict, Depends(get_user_meta)]):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}',
            "username": meta["username"]
        }

        response = requests.get(f'{MICROSERVICE_AUTH_URL}/get-all-users', headers=headers)

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')


@router.get('/book/get-books')
@require_permission(["READ_BOOK"])
def forward_bookmanager_request(meta: Annotated[dict, Depends(get_user_meta)]):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}',
            "username": meta["username"]
        }
        response = requests.get(f'{MICROSERVICE_BOOKMANAGER_URL}/book/get-books', headers=headers)

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
