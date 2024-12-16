'''Зависимости'''


from fastapi import Request, Depends, status, HTTPException
from jwt import decode, PyJWTError
from datetime import datetime, timezone

from src.services.users_service import UsersService
from src.repositories.users_repository import UsersRepository
from src.services.base_users_service import AbstractUsersService
from src.configs.env_config import get_auth_data


auth_data = get_auth_data()


def users_service() -> AbstractUsersService:
    '''Возвращает сервис для работы с пользователями'''
    return UsersService(UsersRepository)


def get_token(request: Request):
    '''Проверяет наличие токена и возвращает его'''
    token = request.cookies.get(auth_data['access_cookie_name'])
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

def get_payload_token(token: str = Depends(get_token)):
    '''Проверяет валидность токена и возвращает его данные.'''
    try:
        payload = decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is not valid')
    
    # Проверка времени жизни токена.
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    
    return payload