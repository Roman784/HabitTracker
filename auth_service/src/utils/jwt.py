'''Работа с jwt'''


from jwt import encode
from datetime import datetime, timedelta, timezone
from src.configs.env_config import get_auth_data


auth_data = get_auth_data()


def create_access_token(data: dict) -> str:
    '''Создает JWT.'''
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, auth_data['secret_key'], auth_data['algorithm'])
    return encode_jwt