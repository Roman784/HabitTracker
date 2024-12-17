'''Конечные точки для работы с аналитикой'''


from typing import Annotated
from fastapi import APIRouter, Depends, status
from pika import BlockingConnection, ConnectionParameters
import json
import threading
import asyncio
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.message_broker.base_message_broker import AbstractMessageBroker
from src.api.dependencies import message_broker, get_payload_token


analytics_router = APIRouter()


@analytics_router.get('/activity', status_code=status.HTTP_200_OK)
async def get_activity(
    payload: Annotated[any, Depends(get_payload_token)],
    broker: Annotated[AbstractMessageBroker, Depends(message_broker)]
):
    '''Возвращает всю активность пользователя'''
    user_id = payload['id']
    await broker.connect()
    reply_to = await broker.send_message('habits_activity_request', {'user_id': user_id})
    response = await broker.get_response(reply_to)
    await broker.close()
    return response
    
    
    
