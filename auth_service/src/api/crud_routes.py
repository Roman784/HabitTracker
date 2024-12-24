'''Конечные точки для CRUD операций над пользователями'''


from typing import Annotated
from fastapi import APIRouter, Depends, Response, status

from src.services.base_users_service import AbstractUsersService
from src.schemas.user_schemas import UserCredsSchema
from src.api.dependencies import users_service
from src.api.dependencies import get_payload_token, message_broker
from src.configs.env_config import AuthData
from src.message_broker.base_message_broker import AbstractMessageBroker


crud_router = APIRouter()


@crud_router.get('/get', status_code=status.HTTP_200_OK)
async def get(
    users_service: Annotated[AbstractUsersService, Depends(users_service)],
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Возвращает данные пользователя по id'''
    user_id = payload['id']
    user = await users_service.get_by_id(user_id)
    return {'user': user}


@crud_router.get('/get-by-creds', status_code=status.HTTP_200_OK)
async def get_by_creds(
    creds: Annotated[UserCredsSchema, Depends()], 
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    '''Возвращает данные пользователя по персональным данным'''
    user = await users_service.get_by_creds(creds)
    return {'user': user}


@crud_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    data: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)]
):
    '''Создаёт пользователя'''
    user_id = await users_service.create(data)
    return { 'user_id': user_id }


@crud_router.put('/update', status_code=status.HTTP_200_OK)
async def update(
    new_data: Annotated[UserCredsSchema, Depends()],
    users_service: Annotated[AbstractUsersService, Depends(users_service)],
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Обновляет данные пользователя'''
    user_id = payload['id']
    await users_service.update(user_id, new_data)
    return { 'message': 'User updated' }


@crud_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete(
    users_service: Annotated[AbstractUsersService, Depends(users_service)],
    payload: Annotated[any, Depends(get_payload_token)],
    broker: Annotated[AbstractMessageBroker, Depends(message_broker)],
    response: Response
):
    '''Удаляет пользователя'''
    user_id = payload['id']

    await broker.connect()
    reply_to = await broker.send_message('delete_user_habits_request', {'user_id': user_id})
    result = await broker.get_response(reply_to)
    await broker.close()

    if (result['status'] == 'ok'):
        await users_service.delete(user_id)
        response.delete_cookie(AuthData.ACCESS_COOKIE_NAME)
        return { 'message': 'User deleted' }
    else:
        return { 'message': 'User deletion error'}
