from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.models.user_model import BaseModel
from src.databse.database import db_session


class AbstractRepository(ABC):
    '''Абстрактный класс для работы с бд'''
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


class SQLAlchemyRepository(AbstractRepository):
    '''Работа с бд через SQLAlchemy'''
    model: BaseModel = None

    async def create(self, data: dict) -> int:
        '''Создаёт запись в бд и возвращает её id'''
        async with db_session() as session:
            record: BaseModel = self.model(**data)
            session.add(record)
            await session.flush()
            await session.commit()
            return record.id

    async def get_by(self, filter_by: dict) -> List[BaseModel]:
        '''Возвращает список записей по указанному фильтру'''
        async with db_session() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    async def update(self, record_id: int, new_data: dict):
        '''Обновляет данные записи'''
        async with db_session() as session:
            record = await self.get_by_id(record_id, session)
            for key, value in new_data.items():
                setattr(record, key, value)
            await session.commit()

    async def delete(self, record_id: int):
        '''Удаляет запись'''
        async with db_session() as session:
            record = await self.get_by_id(record_id, session)
            await session.delete(record)
            await session.commit()


    async def get_by_id(self, record_id: int, session: AsyncSession):
        '''Возвращает запись по id в заданной сессии'''
        query = select(self.model).where(self.model.id == record_id)
        result = await session.execute(query)
        record = result.scalar_one_or_none()

        if record is None:
            raise ValueError(f"Record with id: {record_id} not found")
        
        return record

