'''Работа с jwt'''


from jwt import encode, decode, PyJWTError
from datetime import datetime, timedelta, timezone


def create_access_token(data: dict) -> str:
    '''Создает JWT.'''
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, 'secret_key', 'HS256')
    return encode_jwt