import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token signature")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Error decoding token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_user_meta(token: str = Depends(oauth2_scheme)) -> dict:

    payload = decode_jwt(token)

    permission = payload.get("permissions", [])

    username = payload.get("username")

    if not permission:
        raise HTTPException(status_code=403, detail="User role not found in token")

    meta = {
        "permissions": permission,
        "username": username,
    }

    return meta






