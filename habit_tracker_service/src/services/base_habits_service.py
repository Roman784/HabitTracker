'''Базовый интерфейс для работы с сервисами привычек'''


from abc import ABC, abstractmethod
from typing import List

from src.models.habits_model import HabitsModel
from src.schemas.habits_schemas import HabitsActivitySchema


class AbstractHabitsService(ABC):
    '''Интерфейс для работы с сервисами привычек'''
    @abstractmethod
    async def mark_fulfillment():
        '''Отмечает выполнение привычки'''
        raise NotImplemented

    @abstractmethod
    async def create() -> int:
        '''Создаёт привычку и возвращает её id'''
        raise NotImplemented

    @abstractmethod
    async def get_by_id() -> HabitsModel:
        '''Возвращает данные привычки по id'''
        raise NotImplemented

    @abstractmethod
    async def get_all() -> List[HabitsModel]:
        '''Возвращает все привычки'''
        raise NotImplemented

    @abstractmethod
    async def get_all_activity() -> List[HabitsActivitySchema]:
        '''Возвращает всю активность по дням'''
        raise NotImplemented

    @abstractmethod
    async def update():
        '''Обновляет данные привычки'''
        raise NotImplemented

    @abstractmethod
    async def delete():
        '''Удаляет привычку'''
        raise NotImplemented
    
    @abstractmethod
    async def delete_all():
        '''Удаляет все привычки пользователя'''
        raise NotImplemented
