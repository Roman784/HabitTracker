'''Точка входа в сервис авторизации'''


from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from src.databse.database import create_tables, delete_tables
from src.repositories.users_repository import UsersRepository
from src.services.users_service import UsersService
from src.schemas.user_schemas import UserCredsSchema
from src.api.dependencies import users_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/get')
async def get(
    user_id: int, 
    users_service: Annotated[UsersService, Depends(users_service)]
):
    user = await users_service.get_by_id(user_id)
    return {'user': user}

@app.get('/get-by-creds')
async def get(
    creds: Annotated[UserCredsSchema, Depends()], 
    users_service: Annotated[UsersService, Depends(users_service)]
):
    user = await users_service.get_by_creds(creds)
    return {'user': user}

@app.post('/create')
async def create(
    data: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[UsersService, Depends(users_service)]
):
    user_id = await users_service.create(data)
    return { 'user_id': user_id }

@app.put('/update')
async def create(
    user_id: int, 
    new_data: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[UsersService, Depends(users_service)]
):
    await users_service.update(user_id, new_data)
    return { 'message': 'User updated' }

@app.delete('/delete')
async def delete(
    user_id: int,
    users_service: Annotated[UsersService, Depends(users_service)]
):
    await users_service.delete(user_id)
    return { 'message': 'User deleted' }