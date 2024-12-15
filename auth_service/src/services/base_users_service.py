'''Базовый интерфейс для работы с сервисами пользователей'''


from abc import ABC, abstractmethod

from src.models.user_model import UserModel


class AbstractUsersService(ABC):
    '''Интерфейс для работы с сервисами пользователей'''
    @abstractmethod
    async def create() -> int:
        '''Создаёт пользователя и возвращает его id'''
        raise NotImplemented

    @abstractmethod
    async def get_by_id() -> UserModel:
        '''Возвращает данные пользователя по id'''
        raise NotImplemented

    @abstractmethod
    async def get_by_creds() -> UserModel:
        '''Возвращает данные пользователя по id'''
        raise NotImplemented

    @abstractmethod
    async def update():
        '''Обновляет данные пользователя'''
        raise NotImplemented

    @abstractmethod
    async def delete():
        '''Удаляет пользователя'''
        raise NotImplemented