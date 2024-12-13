'''Точка входа в сервис авторизации'''


from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends, status
from .schemas.user_schema import User, UserResponse, UserCreateResponse
from .schemas.message_schema import MessageResponse
from .storage.repositories.user_repository import UserRepository
from .storage.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/get-one', status_code=status.HTTP_200_OK)
async def get_one(user_id: int) -> UserResponse:
    '''Возвращает данные пользователя'''
    user = await UserRepository.get_one(user_id)
    return user

@app.post('/create', status_code=status.HTTP_201_CREATED)
async def create(user_data: Annotated[User, Depends()]) -> UserCreateResponse:
    '''Создаёт пользователя'''
    user = await UserRepository.create(user_data)
    return { "message": "User created", "user_id": user.id }

@app.put('/update', status_code=status.HTTP_200_OK)
async def update(user_id: int, user_data: Annotated[User, Depends()]) -> MessageResponse:
    '''Обновляет данные пользователя'''
    await UserRepository.update(user_id, user_data)
    return { "message": "User updated" }

@app.delete('/delete', status_code=status.HTTP_200_OK)
async def delete(user_id: int) -> MessageResponse:
    '''Удаляет пользователя'''
    await UserRepository.delete(user_id)
    return { "message": "User deleted" }
