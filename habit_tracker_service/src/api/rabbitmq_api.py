from typing import Annotated
from fastapi import Depends
import json
from pika import BlockingConnection, ConnectionParameters
import asyncio

from src.services.base_habits_service import AbstractHabitsService
from src.api.dependencies import habits_service
from src.api.dependencies import get_payload_token


connection_params = ConnectionParameters(
    host='localhost',
    port=5672,
)


def process_message(ch, method, properties, body):
     asyncio.run(send_response(int(body.decode())))
     ch.basic_ack(delivery_tag=method.delivery_tag)


async def send_response(user_id: int):
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='response')
            response = json.dumps(await get_all(user_id))
            ch.basic_publish(exchange='',
                            routing_key='response',
                            body=response)


def get_request():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='request')
            ch.basic_consume(
                queue='request',
                on_message_callback=process_message
            )
            ch.start_consuming()


async def get_all(user_id: int):
    '''Возвращает данные пользователя по id'''
    service = habits_service()
    habits = await service.get_all(user_id)
    habits_response = [row.to_read_model().model_dump() for row in habits]
    return {'habits': habits_response}