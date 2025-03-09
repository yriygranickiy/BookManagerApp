import uuid

from fastapi import APIRouter, HTTPException
from starlette import status

from app_authorization.models.authorization_models import Roles, Permissions
from app_authorization.repositories.auth_repository import RoleRepository, PermissionRepository
from app_authorization.schemas.user_schema import RoleRequest, RoleResponse, PermissionRequest, PermissionResponse
from app_authorization.services.auth_service import RoleService, PermissionService
from db.database import SessionLocal

router = APIRouter(prefix="/admin", tags=["RoleAndPermission"])
db = SessionLocal()
role_repository = RoleRepository(db)
permission_repository = PermissionRepository(db)
role_service = RoleService(role_repository)
permission_service = PermissionService(permission_repository)


@router.post("/create-role", status_code=status.HTTP_201_CREATED,)
def create_role(data: RoleRequest):
    role = Roles(name=data.name)
    role_service.create(role)
    return f'Successfully created role: {role.name}'

@router.post("/create-permission", status_code=status.HTTP_201_CREATED,)
def create_permission(data: PermissionRequest):
    permission = Permissions(name=data.name)
    permission_service.create(permission)
    return f'Successfully created permission: {permission.name}'

@router.post("/add-permission-to-role",status_code=status.HTTP_201_CREATED)
def add_permission_to_role(role_id: uuid.UUID, permission_id: uuid.UUID):
    permission_service.add_permission_to_role(role_id=role_id, permission_id=permission_id)

@router.post("/add-role-to-user", status_code=status.HTTP_201_CREATED)
def add_role_to_user(user_id: uuid.UUID, role_id: uuid.UUID):
    role_service.add_role_to_user(user_id=user_id, role_id=role_id)

@router.get("/get-all-permissions", status_code=status.HTTP_200_OK, response_model=list[PermissionResponse])
def get_all_permissions():
    return permission_service.get_all()
@router.get("/get-all-roles", status_code=status.HTTP_200_OK, response_model=list[RoleResponse])
def get_all_role():
    return role_service.get_all()


@router.put("/update-permission", status_code=status.HTTP_200_OK)
def update_permission(id_permission: uuid.UUID, data: dict):
    permission = permission_service.get_by_id(id_permission)
    if permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permission with id: {id_permission} "
                                                                          f"not found")
    permission_service.update(id_permission, data)
    return f'Successfully updated permission'

@router.put("/update-role", status_code=status.HTTP_200_OK)
def update_role(role_id: uuid.UUID, data: dict):
    role = role_service.get_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    role_service.update(role_id, data)
    return f'Successfully updated role!'

@router.delete("/delete-permission/{id_permission}", status_code=status.HTTP_204_NO_CONTENT)
def remove_permission(id_permission: uuid.UUID):
    permission = permission_service.get_by_id(id_permission)
    if permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permission with id: {id_permission} "
                                                                          f"not found")
    permission_service.delete(id_permission)
@router.delete("/delete-role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_role(role_id: uuid.UUID):
    role = role_service.get_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    role_service.delete(role_id)


