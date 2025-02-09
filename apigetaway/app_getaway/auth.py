import os
from typing import Dict

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

security = HTTPBearer()

def verify_token(token:str) -> Dict:
    try:
        payload = jwt.decode(token,os.getenv('JWT_SECRET'),os.getenv('JWT_ALGORITHM'))
        return payload
    except JWTError:
        raise HTTPException(status_code=401,detail='Token is invalid')


def get_current_user(credentials=Depends(security)) -> Dict:
    token = credentials.credantials
    return verify_token(token)