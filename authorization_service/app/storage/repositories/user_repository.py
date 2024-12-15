'''Функции для работы с бд'''


from sqlalchemy import select
from fastapi import HTTPException
from app.storage.database import db_session
from app.storage.models.user_model import UserModel
from app.schemas.user_schema import User
from app.logging.logger_factory import get_user_repository_logger
from app.utils.password_hashing import hash_password, verify_password


logger = get_user_repository_logger()


class UserRepository:
    '''Методы для работы с бд пользователей'''
    @staticmethod
    async def get_by_creds(username: str, password: str) -> UserModel:
        '''Возвращает пользователя с определённым именем и паролем'''
        logger.info("Retrieving the user by username: %s", username)
        async with db_session() as session:
            query = select(UserModel).where(UserModel.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user is None:
                logger.warning("User name: %s not found", username)
                raise HTTPException(status_code=404, detail="User not found")

            if not verify_password(password, user.password):
                logger.warning("User name: %s entered the incorrect password", username)
                raise HTTPException(status_code=401, detail="Incorrect password")
            
            return user

    @staticmethod
    async def get_one(user_id: int) -> UserModel:
        '''Возвращает пользователя'''
        logger.info("Retrieving the user, id: %d", user_id)
        async with db_session() as session:
            user = await session.get(UserModel, user_id)

            if user is None:
                logger.warning("User id: %d not found", user_id)
                raise HTTPException(status_code=404, detail="User not found")

            logger.info("User id: %d successfully retrieved", user_id)
            return user

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

            query = select(UserModel).where(UserModel.username == user.username)
            result = await session.execute(query)
            existing_user = result.one_or_none()

            if existing_user:
                logger.warning("User name: %s already exists", data.username)
                raise HTTPException(status_code=400, detail="User already exists")

            session.add(user)
            await session.flush()
            await session.commit()

            logger.info("User id: %d successfully created", user.id)
            return user

    @staticmethod
    async def update(user_id: int, data: User):
        '''Обновляет данные пользователя'''
        logger.info("Updating the user, id: %d", user_id)
        async with db_session() as session:
            user = await session.get(UserModel, user_id)

            if user is None:
                logger.warning("User id: %d not found", user_id)
                raise HTTPException(status_code=404, detail="User not found")

            user.username = data.username
            user.password = hash_password(data.password)
            await session.commit()

            logger.info("User id: %d successfully updated", user_id)

    @staticmethod
    async def delete(user_id: int):
        '''Удаляет пользователя'''
        logger.info("Deleting the user, id: %d", user_id)
        async with db_session() as session:
            user = await session.get(UserModel, user_id)

            if user is None:
                logger.warning("User id: %d not found", user_id)
                raise HTTPException(status_code=404, detail="User not found")

            await session.delete(user)
            await session.commit()

            logger.info("User id: %d successfully deleted", user_id)
