'''Зависимости'''


from fastapi import Request, Depends, status, HTTPException
from jwt import decode, PyJWTError
from datetime import datetime, timezone

from src.services.habits_service import HabitsService
from src.repositories.habits_repository import HabitsRepository, HabitsCalendarRepository
from src.services.base_habits_service import AbstractHabitsService
from src.configs.env_config import get_auth_data
from src.message_broker.base_message_broker import AbstractMessageBroker
from src.message_broker.rabbitmq_broker import RabbitMQBroker


auth_data = get_auth_data()


def habits_service() -> AbstractHabitsService:
    '''Возвращает текущий сервис для работы с привычками'''
    return HabitsService(HabitsRepository, HabitsCalendarRepository)


def message_broker()-> AbstractMessageBroker:
    '''Возвращает текущий брокер сообщений'''
    return RabbitMQBroker()


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
