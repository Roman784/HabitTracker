'''Интерфейс для брокера сообщений'''


from abc import ABC, abstractmethod


class AbstractMessageBroker(ABC):
    '''Интерфейс для брокера сообщений'''
    @abstractmethod
    async def connect():
        '''Подключение, открытие канала'''
        raise NotImplemented


    @abstractmethod
    async def close():
        '''Закрытие подключения и канала'''
        raise NotImplemented


    @abstractmethod
    async def send_message():
        '''Отправка сообщения'''
        raise NotImplemented


    @abstractmethod
    async def get_response():
        '''Прослушивает очередь и возвращает ответ из неё'''
        raise NotImplemented


    @abstractmethod
    async def consume():
        '''Прослушивает очередь и вызывает callback для обработки сообщения'''
        raise NotImplemented
