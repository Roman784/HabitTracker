'''CRUD операции над пользователями'''


from typing import Annotated
from fastapi import Depends, status, APIRouter
from app.schemas.user_schema import User, UserResponse
from app.storage.repositories.user_repository import UserRepository


crud_router = APIRouter()


@crud_router.get('/get-one', status_code=status.HTTP_200_OK)
async def get_one(user_id: int) -> UserResponse:
    '''Возвращает данные пользователя'''
    user = await UserRepository.get_one(user_id)
    return user

@crud_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(user_data: Annotated[User, Depends()]):
    '''Создаёт пользователя'''
    user = await UserRepository.create(user_data)
    return { "message": "User created", "user_id": user.id }

@crud_router.put('/update', status_code=status.HTTP_200_OK)
async def update(user_id: int, user_data: Annotated[User, Depends()]):
    '''Обновляет данные пользователя'''
    await UserRepository.update(user_id, user_data)
    return { "message": "User updated" }

@crud_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete(user_id: int):
    '''Удаляет пользователя'''
    await UserRepository.delete(user_id)
    return { "message": "User deleted" }