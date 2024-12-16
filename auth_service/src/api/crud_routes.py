
from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.services.base_users_service import AbstractUsersService
from src.schemas.user_schemas import UserCredsSchema
from src.api.dependencies import users_service


crud_router = APIRouter()


@crud_router.get('/get', status_code=status.HTTP_200_OK)
async def get(
    user_id: int, 
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    user = await users_service.get_by_id(user_id)
    return {'user': user}

@crud_router.get('/get-by-creds', status_code=status.HTTP_200_OK)
async def get(
    creds: Annotated[UserCredsSchema, Depends()], 
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    user = await users_service.get_by_creds(creds)
    return {'user': user}

@crud_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    data: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    user_id = await users_service.create(data)
    return { 'user_id': user_id }

@crud_router.put('/update', status_code=status.HTTP_200_OK)
async def update(
    user_id: int, 
    new_data: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    await users_service.update(user_id, new_data)
    return { 'message': 'User updated' }

@crud_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete(
    user_id: int,
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    await users_service.delete(user_id)
    return { 'message': 'User deleted' }