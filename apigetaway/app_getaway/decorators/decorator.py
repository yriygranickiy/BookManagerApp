from functools import wraps
from typing import Callable, Annotated

from fastapi import Depends, HTTPException

from app_getaway.security.auth import get_user_meta


def require_permission(allowed_permissions: list):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, meta: Annotated[dict, Depends(get_user_meta)], **kwargs):
            permission = meta.get('permissions', [])
            print(f'User permission: {permission} ', f'Allowed permissions: {allowed_permissions}')
            if not permission or not set(allowed_permissions).intersection(set(permission)):
                raise HTTPException(status_code=403, detail="Access denied")

            return func(*args, meta, **kwargs)

        return wrapper

    return decorator
