'''Работа с jwt'''


from jwt import encode, decode, PyJWTError
from datetime import datetime, timedelta, timezone
from fastapi import Request, Depends, HTTPException, status
from app.configs.env_config import get_auth_data


auth_data = get_auth_data()


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

    encode_jwt = encode(to_encode, auth_data['secret_key'], auth_data['algorithm'])
    return encode_jwt


def get_token(request: Request):
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
