'''Брокер сообщений - rabbitmq'''


from aio_pika import connect, Message, IncomingMessage
from asyncio import sleep
from json import dumps, loads

from .base_message_broker import AbstractMessageBroker


class RabbitMQBroker(AbstractMessageBroker):
    '''Брокер сообщений'''
    def __init__(self):
        '''init'''
        self.__connection = None
        self.__channel = None

        # Нужна для функции get_response.
        # Если её установить локально в функции, то при асинхронной работе, на второй вызов,
        # она навсегда становится None.
        self.__response = None


    async def connect(self):
        '''Подключение, открытие канала'''
        self.__connection = await connect(host='localhost', port=5672)
        self.__channel = await self.__connection.channel()


    async def close(self):
        '''Закрытие подключения и канала'''
        if self.__channel and not self.__channel.is_closed:
            await self.__channel.close()
        if self.__connection and not self.__connection.is_closed:
            await self.__connection.close()


    async def send_message(self, routing_key: str, data: dict = {}):
        '''Отправка сообщения'''
        message_body: bytes = dumps(data).encode()
        reply_to: str = routing_key + '_response'
        message = Message(body=message_body, reply_to=reply_to)

        await self.__channel.default_exchange.publish(
            message=message,
            routing_key=routing_key,
        )

        return reply_to


    async def get_response(self, queue_name: str):
        '''Прослушивает очередь и возвращает ответ из неё'''
        async def on_response(message: IncomingMessage):
            '''Обрабатывает сообщение, устанавливает значение response'''
            async with message.process():
                self.__response = loads(message.body)

        await self.consume(queue_name, on_response)

        # Ожидание ответа.
        while self.__response is None:
            await sleep(0.1)

        return self.__response


    async def consume(self, queue_name: str, callback):
        '''Прослушивает очередь и вызывает callback для обработки сообщения'''
        queue = await self.__channel.declare_queue(queue_name)
        await queue.consume(callback)
