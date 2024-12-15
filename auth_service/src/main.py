'''Точка входа в сервис авторизации'''


from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from src.databse.database import create_tables, delete_tables
from src.repositories.users_repository import UsersRepository
from src.schemas.user_schemas import UserCredsSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/get')
async def get(name: str):
    user = await UsersRepository().get_by({'name': name})
    return {'users': user}

@app.post('/create')
async def create(data: Annotated[UserCredsSchema, Depends()]):
    user_dict = data.model_dump()
    user_id = await UsersRepository().create(user_dict)
    return { 'user_id': user_id }

@app.put('/update')
async def create(user_id: int, new_data: Annotated[UserCredsSchema, Depends()]):
    user_dict = new_data.model_dump()
    await UsersRepository().update(user_id, user_dict)
    return { 'message': 'User updated' }

@app.delete('/delete')
async def delete(user_id: int):
    await UsersRepository().delete(user_id)
    return { 'message': 'User deleted' }