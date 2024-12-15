'''Вход и регистрация'''


from typing import Annotated
from fastapi import Depends, status, APIRouter, Response
from app.schemas.user_schema import User
from app.storage.repositories.user_repository import UserRepository
from app.utils.jwt import create_access_token_for_user


auth_router = APIRouter()


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(creds: Annotated[User, Depends()], response: Response):
    '''Регистрирует нового пользователя'''
    user = await UserRepository.create(creds)

    token = create_access_token_for_user(user.id, user.username)
    response.set_cookie('access_token', token, httponly=True)

    return { 'message': 'User registered', 'user_id': user.id, 'access_token': token }


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(creds: Annotated[User, Depends()], response: Response):
    '''Авторизует пользователя'''
    user = await UserRepository.get_by_creds(creds.username, creds.password)

    token = create_access_token_for_user(user.id, user.username)
    response.set_cookie('access_token', token, httponly=True)

    return { 'message': 'User logged in', 'access_token': token }


@auth_router.post('/logout', status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    response.delete_cookie(key='access_token')
    return { 'message': 'User logged out '}
