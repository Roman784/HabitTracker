'''Брокер сообщений - rabbitmq'''


from aio_pika import connect, Message, IncomingMessage
from asyncio import sleep
from json import dumps, loads

from .base_message_broker import AbstractMessageBroker
from src.configs.env_config import MessageBrokerData
from src.logging.message_broker_logger import MessageBrokerLogger


logger = MessageBrokerLogger().get_logger()


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

        logger.info('Broker inited %d', id(self))


    async def connect(self):
        '''Подключение, открытие канала'''
        while True:
            try:
                self.__connection = await connect(host=MessageBrokerData.HOST, port=MessageBrokerData.PORT)
                self.__channel = await self.__connection.channel()
                break
            except:
                logger.warning('Connection error %d', id(self))
                await sleep(0.5)

        logger.info('Broker connected %d', id(self))


    async def close(self):
        '''Закрытие подключения и канала'''
        if self.__channel and not self.__channel.is_closed:
            await self.__channel.close()
        if self.__connection and not self.__connection.is_closed:
            await self.__connection.close()
        
        logger.info('Broker closed %d', id(self))


    async def send_message(self, routing_key: str, data: dict = {}):
        '''Отправка сообщения'''
        logger.info('Sending a message from %d to %s', id(self), routing_key)
        message_body: bytes = dumps(data).encode()
        reply_to: str = routing_key + '_response'
        message = Message(body=message_body, reply_to=reply_to)

        await self.__channel.default_exchange.publish(
            message=message,
            routing_key=routing_key,
        )

        logger.info('Message sended from %d to %s', id(self), routing_key)
        return reply_to


    async def get_response(self, queue_name: str):
        '''Прослушивает очередь и возвращает ответ из неё'''
        logger.info('Receiving a response from %s to %d', queue_name, id(self))
        async def on_response(message: IncomingMessage):
            '''Обрабатывает сообщение, устанавливает значение response'''
            async with message.process():
                self.__response = loads(message.body)

        await self.consume(queue_name, on_response)

        # Ожидание ответа.
        while self.__response is None:
            await sleep(0.1)

        logger.info('Message received from %s to %d', queue_name, id(self))
        return self.__response


    async def consume(self, queue_name: str, callback):
        '''Прослушивает очередь и вызывает callback для обработки сообщения'''
        logger.info('Comsuming %d', id(self))
        queue = await self.__channel.declare_queue(queue_name)
        await queue.consume(callback)
