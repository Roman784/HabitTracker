'''Работа с jwt'''


from jwt import encode
from datetime import datetime, timedelta, timezone
from src.configs.env_config import AuthData


def create_access_token(data: dict) -> str:
    '''Создает JWT.'''
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, AuthData.SECRET_KEY, AuthData.ALGORITHM)
    return encode_jwt
