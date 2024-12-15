'''Работа с jwt'''


from jwt import encode, decode, PyJWTError
from datetime import datetime, timedelta, timezone
from os import getenv
from dotenv import load_dotenv
from fastapi import Request, Depends, HTTPException, status


load_dotenv()
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = getenv('JWT_ALGORITHM')
JWT_ACCESS_COOKIE_NAME = getenv('JWT_ACCESS_COOKIE_NAME')


def create_access_token_for_user(user_id: int, username: str) -> str:
    '''Создаёт JWT для пользователя'''
    return create_access_token({
        'id': user_id,
        'username': username
    })


def create_access_token(data: dict) -> str:
    '''Создает JWT.'''
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encode_jwt


def get_token(request: Request):
    token = request.cookies.get(JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

def get_payload_token(token: str = Depends(get_token)):
    '''Проверяет валидность токена и возвращает его данные.'''
    try:
        payload = decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is not valid')
    
    # Проверка времени жизни токена.
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    
    return payload
