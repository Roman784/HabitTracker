'''Работа с jwt'''


import jwt
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv


load_dotenv()
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def create_access_token_for_user(user_id: int, username: str) -> str:
    '''Создаёт JWT для пользователя'''
    return create_access_token({
        "id": user_id,
        "username": username
    })


def create_access_token(data: dict) -> str:
    '''Создает JWT.'''
    payload = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token: str):
    '''Проверяет валидность токена и возвращает его данные.'''
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None