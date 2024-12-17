'''Конечные точки для работы с аналитикой'''


from typing import Annotated
from fastapi import APIRouter, Depends, status
from pika import BlockingConnection, ConnectionParameters
import json
import threading
import asyncio

from src.api.dependencies import get_payload_token


analytics_router = APIRouter()


connection_params = ConnectionParameters(
    host='localhost',
    port=5672,
)


response_queue = asyncio.Queue()


def process_message(ch, method, properties, body):
    asyncio.run(response_queue.put(body.decode()))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_request(user_id: int):
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='request')
            ch.basic_publish(exchange='',
                             routing_key='request',
                             body=str(user_id))


def get_response():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='response')
            ch.basic_consume(
                queue='response',
                on_message_callback=process_message
            )
            ch.start_consuming()
    


@analytics_router.get('/activity', status_code=status.HTTP_200_OK)
async def get_activity(
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Возвращает всю активность пользователя'''
    user_id = payload['id']
    threading.Thread(target=get_response).start()
    send_request(user_id)
    response = await response_queue.get()
    return json.loads(response)
    
    
    
