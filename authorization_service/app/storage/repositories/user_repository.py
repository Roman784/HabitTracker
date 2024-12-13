'''Функции для работы с бд'''


import logging
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from ..database import db_session
from ..models.user_model import UserModel
from ...schemas.user_schema import User


load_dotenv()
DATABASE_URL = getenv('DB_PATH')
LOGS_FILE_NAME = getenv('REPOSITORY_LOGS_FILE')

logging.basicConfig(
    filename=LOGS_FILE_NAME,
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger('user_repository')


class UserRepository:
    '''Методы для работы с бд пользователей'''
    @classmethod
    async def get_one(cls, user_id: int) -> UserModel:
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

    @classmethod
    async def create(cls, data: User) -> UserModel:
        '''Создаёт пользователя'''
        logger.info("Creating new user, name: %s", data.username)
        async with db_session() as session:
            user = UserModel(
                username=data.username,
                password=data.password
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

    @classmethod
    async def update(cls, user_id: int, data: User):
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

    @classmethod
    async def delete(cls, user_id: int):
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
