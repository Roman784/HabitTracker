'''Базовый интерфейс для работы с бд'''


from abc import ABC, abstractmethod
from typing import List

from src.models.user_model import BaseModel


class AbstractRepository(ABC):
    '''Интерфейс для работы с бд'''
    model: BaseModel = None

    @abstractmethod
    async def create() -> int:
        '''Создаёт запись в бд и возвращает её id'''
        raise NotImplemented

    @abstractmethod
    async def get_by() -> List[BaseModel]:
        '''Возвращает список записей по указанному фильтру'''
        raise NotImplemented

    @abstractmethod
    async def update():
        '''Обновляет данные записи'''
        raise NotImplemented

    @abstractmethod
    async def delete():
        '''Удаляет запись'''
        raise NotImplemented
