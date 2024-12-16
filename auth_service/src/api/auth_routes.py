'''Конечные точки для работы с авторизацией'''


from typing import Annotated
from fastapi import APIRouter, Depends, Response, status

from src.services.base_users_service import AbstractUsersService
from src.schemas.user_schemas import UserCredsSchema, UserSchema
from src.api.dependencies import users_service
from src.configs.env_config import get_auth_data
from src.utils.jwt import create_access_token


auth_router = APIRouter()
auth_data = get_auth_data()


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(
    creds: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)],
    response: Response
):
    '''Регистрирует нового пользователя'''
    user_id = await users_service.create(creds)
    user = await users_service.get_by_id(user_id)
    token = set_token(user, response)

    return { 'message': 'User registered', 'user_id': user.id, 'access_token': token }


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(
    creds: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)],
    response: Response
):
    '''Авторизует пользователя'''
    user = await users_service.get_by_creds(creds)
    token = set_token(user, response)

    return { 'message': 'User logged in', 'access_token': token }


@auth_router.post('/logout', status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    '''Удаляет куку с токеном у пользователя'''
    response.delete_cookie(auth_data['access_cookie_name'])
    return { 'message': 'User logged out '}


def set_token(user: UserSchema, response: Response) -> str:
    '''Создаёт jwt, устанавливает в куки и возвращает его'''
    token = create_access_token({'id': user.id, 'name': user.name})
    response.set_cookie(auth_data['access_cookie_name'], token)
    return token
