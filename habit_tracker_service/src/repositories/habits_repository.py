'''Работа с бд привычек'''


from src.repositories.sqlalchemy_repository import SQLAlchemyRepository
from src.models.habits_model import HabitsModel, HabitsCalendarModel


class HabitsRepository(SQLAlchemyRepository):
    '''Репзиторий для работы с бд привычек'''
    model = HabitsModel

class HabitsCalendarRepository(SQLAlchemyRepository):
    '''Репзиторий для работы с бд календарем привычек'''
    model = HabitsCalendarModel