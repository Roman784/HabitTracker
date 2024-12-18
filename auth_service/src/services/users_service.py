'''Сервис для работы с пользователями'''


from fastapi import HTTPException, status

from src.services.base_users_service import AbstractUsersService
from src.repositories.base_repository import AbstractRepository
from src.schemas.user_schemas import UserCredsSchema
from src.models.user_model import UserModel
from src.utils.password_hashing import hash_password, verify_password
from src.logging.users_service_logger import UsersServiceLogger


logger = UsersServiceLogger().get_logger()


class UsersService(AbstractUsersService):
    '''Сервис для работы с реальными пользователями'''
    def __init__(self, users_repository: AbstractRepository):
        self.users_repository: AbstractRepository = users_repository()
    
    async def create(self, data: UserCredsSchema) -> int:
        '''Создаёт пользователя и возвращает его id'''
        logger.info('Creating new user, name: %s', data.name)

        data.password = hash_password(data.password)
        user_dict = data.model_dump()

        users = await self.users_repository.get_by({'name': data.name})
        if len(users) != 0:
            logger.warning('User, name: %s, already exists', data.name)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

        user_id = await self.users_repository.create(user_dict)
        logger.info('User, name: %s, successfully created', data.name)
        return user_id
    

    async def get_by_id(self, user_id: int) -> UserModel:
        '''Возвращает данные пользователя по id'''
        logger.info('Retrieving the user, id: %d', user_id)
        users = await self.users_repository.get_by({'id': user_id})

        if len(users) == 0:
            logger.warning('User, id: %d, not found', user_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        user = users[0]
        self.delete_password(user)

        logger.info('User, id: %d, successfully retrieved', user_id)
        return user
    

    async def get_by_creds(self, creds: UserCredsSchema) -> UserModel:
        '''Возвращает данные пользователя по id'''
        logger.info('Retrieving the user, name: %s', creds.name)
        users = await self.users_repository.get_by({'name': creds.name})

        if len(users) == 0:
            logger.warning('User, name: %s, not found', creds.name)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        if not verify_password(creds.password, users[0].password):
            logger.warning('User, name: %s, entered the incorrect password', creds.name)
            raise HTTPException(status_code=401, detail='Incorrect password')

        user = users[0]
        self.delete_password(user)

        logger.info('User, name: %s, successfully retrieved', creds.name)
        return user


    async def update(self, user_id: int, new_data: UserCredsSchema):
        '''Обновляет данные пользователя'''
        logger.info('Updating the user id: %d', user_id)

        users = await self.users_repository.get_by({'name': new_data.name})

        if len(users) != 0:
            logger.warning('The user, name: %s, is already taken', new_data.name)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Name is already taken')

        new_data.password = hash_password(new_data.password)
        user_dict = new_data.model_dump()
        try:
            await self.users_repository.update(user_id, user_dict)
            logger.info('User, id: %d, successfully updated', user_id)
        except ValueError as e:
            logger.warning('User, id: %d, not found', user_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


    async def delete(self, user_id: int):
        '''Удаляет пользователя'''
        logger.info('Deleting the user id: %d', user_id)
        try:
            await self.users_repository.delete(user_id)
            logger.info('User, id: %d, successfully deleted', user_id)
        except ValueError as e:
            logger.warning('User, id: %d, not found', user_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    def delete_password(self, user: UserModel):
        '''Удаляет поле с паролем'''
        del user.password
