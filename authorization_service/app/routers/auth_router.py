'''Вход и регистрация'''


from typing import Annotated
from fastapi import Depends, status, APIRouter, Response
from authx import AuthX, AuthXConfig
from app.schemas.user_schema import User, UserResponse
from app.storage.repositories.user_repository import UserRepository
from app.utils.jwt import create_access_token_for_user


auth_router = APIRouter()


config = AuthXConfig()
config.JWT_SECRET_KEY = 'Secret_key'
config.JWT_ACCESS_COOKIE_NAME = 'access_token'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(creds: Annotated[User, Depends()], response: Response):
    '''Авторизует пользователя'''
    user = await UserRepository.get_by_creds(creds.username, creds.password)

    token = security.create_access_token(uid=str(user.id), data={"username": user.username})
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)

    return { "message": "User logged in", "access_token": token }


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(creds: Annotated[User, Depends()], response: Response):
    '''Регистрирует нового пользователя'''
    user = await UserRepository.create(creds)

    token = security.create_access_token(uid=str(user.id), data={"username": user.username})
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)

    return { "message": "User registered", "user_id": user.id, "access_token": token }


@auth_router.get("/get", dependencies=[Depends(security.access_token_required)])
def get():
    return "hello"
