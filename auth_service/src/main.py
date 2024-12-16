'''Точка входа в сервис авторизации'''


from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Response

from src.databse.database import create_tables, delete_tables
from src.services.base_users_service import AbstractUsersService
from src.schemas.user_schemas import UserCredsSchema
from src.api.dependencies import users_service
from src.utils.jwt import create_access_token
from src.configs.env_config import get_auth_data


auth_data = get_auth_data()


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/register')
async def register_user(
    creds: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)],
    response: Response
):
    '''Регистрирует нового пользователя'''
    user_id = await users_service.create(creds)
    user = await users_service.get_by_id(user_id)

    token = create_access_token({'id': user.id, 'name': user.name})
    response.set_cookie(auth_data['access_cookie_name'], token)

    return { 'message': 'User registered', 'user_id': user.id, 'access_token': token }


@app.post('/login')
async def login_user(
    creds: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)],
    response: Response
):
    '''Авторизует пользователя'''
    user = await users_service.get_by_creds(creds)

    token = create_access_token({'id': user.id, 'name': user.name})
    response.set_cookie(auth_data['access_cookie_name'], token)

    return { 'message': 'User logged in', 'access_token': token }


@app.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie(auth_data['access_cookie_name'])
    return { 'message': 'User logged out '}


@app.get('/get')
async def get(
    user_id: int, 
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    user = await users_service.get_by_id(user_id)
    return {'user': user}

@app.get('/get-by-creds')
async def get(
    creds: Annotated[UserCredsSchema, Depends()], 
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    user = await users_service.get_by_creds(creds)
    return {'user': user}

@app.post('/create')
async def create(
    data: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    user_id = await users_service.create(data)
    return { 'user_id': user_id }

@app.put('/update')
async def create(
    user_id: int, 
    new_data: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    await users_service.update(user_id, new_data)
    return { 'message': 'User updated' }

@app.delete('/delete')
async def delete(
    user_id: int,
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    await users_service.delete(user_id)
    return { 'message': 'User deleted' }