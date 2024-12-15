'''Работа с бд пользователей'''


from src.repositories.base_repository import SQLAlchemyRepository
from src.models.user_model import UserModel


class UsersRepository(SQLAlchemyRepository):
    '''Репзиторий для работы с бд пользователей'''
    model = UserModel