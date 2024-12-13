'''Функции для работы с бд'''


from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from ..database import db_session
from ..models.user_model import UserModel
from ...schemas.user_schema import User


class UserRepository:
    '''Методы для работы с бд пользователей'''
    @classmethod
    async def get_one(cls, user_id: int) -> UserModel:
        '''Возвращает пользователя'''
        async with db_session() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            try:
                result = await session.execute(query)
                user = result.scalar_one()
                return user
            except NoResultFound as e:
                raise HTTPException(status_code=404, detail="User not found") from e

    @classmethod
    async def create(cls, data: User) -> UserModel:
        '''Добавляет пользователя'''
        async with db_session() as session:
            user = UserModel(
                username=data.username,
                password=data.password
            )
            try:
                session.add(user)
                await session.flush()
                await session.commit()
                return user
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail="User already exists") from e

    @classmethod
    async def update(cls, user_id: int, data: User):
        '''Обновляет данные пользователя'''
        async with db_session() as session:
            query = (
                update(UserModel)
                .where(UserModel.id == user_id)
                .values(**data.model_dump(exclude_unset=True)))
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")

    @classmethod
    async def delete(cls, user_id: int):
        '''Удаляет пользователя'''
        async with db_session() as session:
            query = delete(UserModel).where(UserModel.id == user_id)
            await session.execute(query)
            await session.commit()
