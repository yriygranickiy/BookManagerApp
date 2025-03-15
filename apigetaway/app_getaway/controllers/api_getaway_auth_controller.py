import os
from typing import Annotated

import requests
from fastapi import APIRouter, HTTPException, Depends

from app_getaway.decorators.decorator import require_permission
from app_getaway.schema.schema import LoginRequest, RegisterRequest
from app_getaway.security.auth import get_user_meta

router = APIRouter(prefix='/apigetaway/auth', tags=['apigetaway_auth'])

IN_DOCKER = os.path.exists("/.dockerenv")
MICROSERVICE_AUTH_URL = "http://app-auth-service:8000/auth" if IN_DOCKER else "http://localhost:8000/auth"
@router.post('/register')
def forward_register_request(data: RegisterRequest):
    try:
        payload = data.model_dump_json()
        if not payload:
            raise HTTPException(status_code=400, detail='Empty payload')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{MICROSERVICE_AUTH_URL}/register', data=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return 'Successfully registration!'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Register service error: {e}')

@router.post('/login')
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
            "permissions": f'{meta["permissions"]}'
        }
        response = requests.get(f'{MICROSERVICE_AUTH_URL}/get-all-users', headers=headers)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')