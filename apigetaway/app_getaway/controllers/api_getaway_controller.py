from typing import Annotated

import httpx
from fastapi import APIRouter, Request, Depends, HTTPException

from app_getaway.decorators.decorator import require_permission
from app_getaway.schema.schema import LoginRequest
from app_getaway.security.auth import get_user_meta

router = APIRouter(prefix='/apigetaway', tags=['apigetaway'])

MICROSERVICE_AUTH_URL = "http://0.0.0.0:8000/auth"
MICROSERVICE_BOOKMANAGER_URL = "http://0.0.0.0:8001/book"

client = httpx.Client()
@router.post('/auth/login')
def forward_auth_request(data: LoginRequest, request: Request):
    try:
        payload = data.model_dump()
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        headers = {
            "Content-Type": "application/json",
            "Authorization": request.headers.get("Authorization", "")
        }
        response = client.post(f'{MICROSERVICE_AUTH_URL}/login', json=payload, headers=headers)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')

@router.get('/auth/get-all-users')
@require_permission(["READ_USER"])
def forward_auth_request_get_all_users(meta: Annotated[dict, Depends(get_user_meta)]):
    try:
        headers = {
            "permissions": f'{meta["permissions"]}',
            "username": meta["username"]
        }
        response = client.get(f'{MICROSERVICE_AUTH_URL}/get-all-users', headers=headers)
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
        response = client.get(f'{MICROSERVICE_BOOKMANAGER_URL}/get-books', headers=headers)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')





