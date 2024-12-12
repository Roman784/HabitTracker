'''Функции для работы с бд'''


from sqlalchemy import select, update, delete
from app.api.storage.storage import db_session, UserTable
from app.api.storage.models import User


class UserRepository:
    '''Методы для работы с бд пользователей'''
    @classmethod
    async def create(cls, data: User) -> UserTable:
        '''Добавляет пользователя'''
        async with db_session() as session:

            user = UserTable(
                username=data.username,
                password=data.password
            )

            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def read(cls, user_id: int) -> UserTable:
        '''Добавляет пользователя'''
        async with db_session() as session:
            query = select(UserTable).where(UserTable.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one()
            return user

    @classmethod
    async def update(cls, user_id: int, data: User):
        '''Обновляет данные пользователя'''
        async with db_session() as session:
            query = (
                update(UserTable)
                .where(UserTable.id == user_id)
                .values(**data.model_dump(exclude_unset=True)))
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, user_id: int):
        '''Удаляет пользователя'''
        async with db_session() as session:
            query = delete(UserTable).where(UserTable.id == user_id)
            await session.execute(query)
            await session.commit()
