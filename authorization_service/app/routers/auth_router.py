'''Вход и регистрация'''


from typing import Annotated
from fastapi import Depends, status, APIRouter, Response
from pydantic import Tok
from app.schemas.user_schema import User, UserResponse
from app.storage.repositories.user_repository import UserRepository
from app.utils.jwt import create_access_token_for_user


auth_router = APIRouter()


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user_data: Annotated[User, Depends()], response: Response):
    '''Регистрирует новго пользователя'''
    user = await UserRepository.create(user_data)

    access_token = create_access_token_for_user(user.id, user.username)
    response.set_cookie("access_token", access_token)

    return { "message": "User registered", "user_id": user.id, "access_token": access_token }


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(user_data: Annotated[User, Depends()], response: Response):
    '''Авторизует пользователя'''
    user = await UserRepository.get_by_username_and_password(user_data.username, user_data.password)

    access_token = create_access_token_for_user(user.id, user.username)
    response.set_cookie("access_token", access_token)

    return { "message": "User logged in", "access_token": access_token }
