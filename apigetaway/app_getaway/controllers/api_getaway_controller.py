import http.client
from typing import Annotated

import requests


from fastapi import APIRouter, Request, Depends, HTTPException

from app_getaway.decorators.decorator import require_permission
from app_getaway.schema.schema import LoginRequest
from app_getaway.security.auth import get_user_meta

router = APIRouter(prefix='/apigetaway', tags=['apigetaway'])

# TODO: docker compose links / depends on / network глянуть разницу  
MICROSERVICE_AUTH_URL = "http://app-auth-service:8000"
MICROSERVICE_BOOKMANAGER_URL = "http://0.0.0.0:8001/book"


@router.post('/auth/login')
def forward_auth_request(data: LoginRequest, request: Request):
    try:

        payload = data.model_dump_json()
        print(payload)
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        headers = {
            "Content-Type": "application/json"
        }
        print(headers)
        print("start request")
        # auth_client = http.client.HTTPConnection(MICROSERVICE_AUTH_URL)
        # auth_client.request('POST', '/auth/login', body=payload, headers=headers)

        response = requests.post(f'{MICROSERVICE_AUTH_URL}/auth/login', headers=headers, data=payload)

        print("end request")

        # response = auth_client.getresponse()
        print(response.status_code)
        print(response.text)

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
        # response = client.get(f'{MICROSERVICE_AUTH_URL}/get-all-users', headers=headers)
        # return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')


# @router.get('/book/get-books')
# @require_permission(["READ_BOOK"])
# def forward_bookmanager_request(meta: Annotated[dict, Depends(get_user_meta)]):
#     try:
#         headers = {
#             "permissions": f'{meta["permissions"]}',
#             "username": meta["username"]
#         }
#         response = client.get(f'{MICROSERVICE_BOOKMANAGER_URL}/get-books', headers=headers)
#         return response.json()
#     except Exception as e:
#         raise HTTPException(status_code=502, detail=f'Authorization service error: {e}')





