'''Зависимости'''


from src.services.users_service import UsersService
from src.repositories.users_repository import UsersRepository
from src.services.base_users_service import AbstractUsersService


def users_service() -> AbstractUsersService:
    '''Возвращает сервис для работы с пользователями'''
    return UsersService(UsersRepository)