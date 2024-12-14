'''Функции для работы с бд'''


from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from ..database import db_session
from ..models.user_model import UserModel
from ...schemas.user_schema import User
from ...logging.logger import get_user_repository_logger
from ...utils.password_hashing import hash_password, verify_password


logger = get_user_repository_logger()


class UserRepository:
    '''Методы для работы с бд пользователей'''
    @staticmethod
    async def get_one(user_id: int) -> UserModel:
        '''Возвращает пользователя'''
        logger.info("Retrieving the user, id: %d", user_id)
        async with db_session() as session:
            query = select(UserModel).where(UserModel.id == user_id)
            try:
                result = await session.execute(query)
                user = result.scalar_one()

                logger.info("User id: %d successfully retrieved", user_id)
                return user
            except NoResultFound as e:

                logger.warning("User id: %d not found", user_id)
                raise HTTPException(status_code=404, detail="User not found") from e

    @staticmethod
    async def create(data: User) -> UserModel:
        '''Создаёт пользователя'''
        logger.info("Creating new user, name: %s", data.username)
        async with db_session() as session:
            hashed_password = hash_password(data.password)
            user = UserModel(
                username=data.username,
                password=hashed_password
            )
            try:
                session.add(user)
                await session.flush()
                await session.commit()

                logger.info("User id: %d successfully created", user.id)
                return user
            except IntegrityError as e:
                await session.rollback()

                logger.warning("User name: %s already exists", data.username)
                raise HTTPException(status_code=400, detail="User already exists") from e

    @staticmethod
    async def update(user_id: int, data: User):
        '''Обновляет данные пользователя'''
        logger.info("Updating the user, id: %d", user_id)
        async with db_session() as session:
            query = (
                update(UserModel)
                .where(UserModel.id == user_id)
                .values(username=data.username, password=data.password))
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                logger.warning("User id: %d not found", user_id)
                raise HTTPException(status_code=404, detail="User not found")

            logger.info("User id: %d successfully updated", user_id)

    @staticmethod
    async def delete(user_id: int):
        '''Удаляет пользователя'''
        logger.info("Deleting the user, id: %d", user_id)
        async with db_session() as session:
            query = delete(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                logger.warning("User id: %d not found", user_id)
                raise HTTPException(status_code=404, detail="User not found")

            logger.info("User id: %d successfully deleted", user_id)
