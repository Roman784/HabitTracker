'''Зависимости'''


from src.services.users_service import UsersService
from src.repositories.users_repository import UsersRepository


def users_service():
    '''Возвращает сервис для работы с пользователями'''
    return UsersService(UsersRepository)