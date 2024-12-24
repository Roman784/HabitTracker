'''Инициализация брокеров, их подключение и отключение'''


from typing import List, Tuple

from src.message_broker.base_message_broker import AbstractMessageBroker
from src.api.dependencies import message_broker


# Матрица брокеров.
# Брокер.
# Имя очереди, что брокер слушает.
# Функция, которая обрабатывает приходящие сообщения.
brokers: List[Tuple[AbstractMessageBroker, str, function]] = []


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