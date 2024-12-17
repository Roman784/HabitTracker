'''Инициализация брокеров, их подключение и отключение'''


from typing import List, Tuple

from src.message_broker.base_message_broker import AbstractMessageBroker
from src.api.dependencies import message_broker
from src.api.message_broker_api import on_habits_activity


# Матрица брокеров.
# Брокер.
# Имя очереди, что брокер слушает.
# Функция, которая обрабатывает приходящие сообщения.
brokers: List[Tuple[AbstractMessageBroker, str, any]] = [
    (message_broker(), 'habits_activity_request', on_habits_activity)
]


async def connect_brokers():
    '''Подключение брокеров'''
    for broker, _, _ in brokers:
        await broker.connect()


async def start_consuming():
    '''Запускает прослушивание очередей'''
    for broker, queue_name, func in brokers:
        await broker.consume(queue_name, func)


async def close_brokers():
    '''Отключение брокеров'''
    for broker, _, _ in brokers:
        await broker.close()