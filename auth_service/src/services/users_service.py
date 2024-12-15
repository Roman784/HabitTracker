'''Сервис для работы с пользователями'''


from fastapi import HTTPException, status

from src.services.base_users_service import AbstractUsersService
from src.repositories.base_repository import AbstractRepository
from src.schemas.user_schemas import UserCredsSchema
from src.models.user_model import UserModel
from src.schemas.user_schemas import UserCredsSchema
from src.utils.password_hashing import hash_password, verify_password



class UsersService(AbstractUsersService):
    '''Сервис для работы с реальными пользователями'''
    def __init__(self, users_repository: AbstractRepository):
        self.users_repository: AbstractRepository = users_repository()
    
    async def create(self, data: UserCredsSchema) -> int:
        '''Создаёт пользователя и возвращает его id'''
        data.password = hash_password(data.password)
        user_dict = data.model_dump()

        users = await self.users_repository.get_by({'name': data.name})
        if len(users) != 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

        user_id = await self.users_repository.create(user_dict)
        return user_id
    

    async def get_by_id(self, user_id: int) -> UserModel:
        '''Возвращает данные пользователя по id'''
        users = await self.users_repository.get_by({'id': user_id})

        if len(users) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        return users[0]
    

    async def get_by_creds(self, creds: UserCredsSchema) -> UserModel:
        '''Возвращает данные пользователя по id'''
        users = await self.users_repository.get_by({'name': creds.name})

        if len(users) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        if not verify_password(creds.password, users[0].password):
            raise HTTPException(status_code=401, detail='Incorrect name or password')

        return users[0]


    async def update(self, user_id: int, new_data: UserCredsSchema):
        '''Обновляет данные пользователя'''
        user_dict = new_data.model_dump()
        try:
            await self.users_repository.update(user_id, user_dict)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


    async def delete(self, user_id: int):
        '''Удаляет пользователя'''
        try:
            await self.users_repository.delete(user_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
