'''Сервис для работы с пользователями'''


from src.repositories.base_repository import AbstractRepository
from src.schemas.user_schemas import UserCredsSchema
from src.models.user_model import UserModel
from src.schemas.user_schemas import UserCredsSchema


class UsersService:
    '''Сервис для работы с пользователями'''
    def __init__(self, users_repository: AbstractRepository):
        self.users_repository: AbstractRepository = users_repository()
    
    async def create(self, data: UserCredsSchema) -> int:
        user_dict = data.model_dump()
        user_id = await self.users_repository.create(user_dict)
        return user_id
    
    async def get_by_id(self, user_id: int) -> UserModel:
        '''Возвращает данные пользователя по id'''
        users = await self.users_repository.get_by({'id': user_id})
        return users[0]
    
    async def get_by_creds(self, creds: UserCredsSchema) -> UserModel:
        '''Возвращает данные пользователя по id'''
        users = await self.users_repository.get_by({
            'name': creds.name, 
            'password': creds.password
        })
        return users[0]

    async def update(self, user_id: int, new_data: UserCredsSchema):
        '''Обновляет данные пользователя'''
        user_dict = new_data.model_dump()
        await self.users_repository.update(user_id, user_dict)

    async def delete(self, user_id: int):
        '''Удаляет пользователя'''
        await self.users_repository.delete(user_id)
