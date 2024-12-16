'''Сервис для работы с привычками'''


from fastapi import HTTPException, status
from typing import List
from datetime import date

from src.services.base_habits_service import AbstractHabitsService
from src.repositories.base_repository import AbstractRepository
from src.schemas.habits_schemas import HabitCredsSchema, HabitsCalendarSchema
from src.models.habits_model import HabitsModel
from src.logging.habits_service_logger import HabitsServiceLogger


logger = HabitsServiceLogger().get_logger()


class HabitsService(AbstractHabitsService):
    '''Сервис для работы с реальными привычками'''
    def __init__(self, habits_repository: AbstractRepository, habits_calendar_repository: AbstractRepository):
        self.habits_repository: AbstractRepository = habits_repository()
        self.habits_calendar_repository: AbstractRepository = habits_calendar_repository()


    async def create(self, data: HabitCredsSchema) -> int:
        '''Создаёт привычку и возвращает её id'''
        logger.info('Creating new habit by user, id: %d', data.user_id)

        habit_dict = data.model_dump()

        habits = await self.habits_repository.get_by({'name': data.name})
        if len(habits) != 0:
            logger.warning('Habit, name: %s, already exists', data.name)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Habit already exists')

        habit_id = await self.habits_repository.create(habit_dict)

        await self.create_day_in_calendar(habit_id)

        logger.info('Habit by user, id: %d, successfully created', data.user_id)
        return habit_id
    

    async def get_by_id(self, user_id: int, habit_id: int) -> HabitsModel:
        '''Возвращает данные привычки по id'''
        logger.info('Retrieving the habit, id: %d', habit_id)
        habit: HabitsModel = await self.check_for_accessibility_and_get(user_id, habit_id)

        logger.info('Habit, id: %d, successfully retrieved', habit_id)
        return habit


    async def get_all(self, user_id: int) -> List[HabitsModel]:
        '''Возвращает все привычки'''
        logger.info('Retrieving the all habits by user, id: %d', user_id)
        habits = await self.habits_repository.get_by({'user_id': user_id})

        logger.info('Habits by user, id: %d, successfully retrieved', user_id)
        return habits


    async def update(self, user_id: int, habit_id: int, new_data: HabitCredsSchema):
        '''Обновляет данные привычки'''
        logger.info('Updating the habit, id: %d', habit_id)
        await self.check_for_accessibility_and_get(user_id, habit_id)

        habit_dict = new_data.model_dump()
        try:
            await self.habits_repository.update(habit_id, habit_dict)
            logger.info('Habit, id: %d, successfully updated', habit_id)
        except ValueError as e:
            logger.warning('Habit, id: %d, not found', habit_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


    async def delete(self, user_id: int, habit_id: int):
        '''Удаляет привычку'''
        logger.info('Deleting the habit, id: %d', habit_id)
        await self.check_for_accessibility_and_get(user_id, habit_id)

        try:
            await self.habits_repository.delete(habit_id)
            logger.info('Habit, id: %d, successfully deleted', habit_id)
        except ValueError as e:
            logger.warning('Habit, id: %d, not found', habit_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


    async def check_for_accessibility_and_get(self, user_id: int, habit_id: int) -> HabitsModel:
        '''Проверяет привычку на доступность - корректный ли автор. Возвращает привычку'''
        habit: HabitsModel = await self.check_for_existence_and_get(habit_id)
        if habit.user_id != user_id:
            logger.warning('Habit, id: %d, of another user', habit_id)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Habit of another user')
        return habit

    async def check_for_existence_and_get(self, habit_id: int) -> HabitsModel:
        '''Проверяет наличие привычки в бд и возвращает её, если существует'''
        habits = await self.habits_repository.get_by({'id': habit_id})
        if len(habits) == 0:
            logger.warning('Habit, id: %d, not found', habit_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Habit not found')
        return habits[0]


    async def create_day_in_calendar(self, habit_id: int):
        '''Создаёт запись в бд календаря с сегодняшней датой'''
        logger.info('Creating new day by habit, id: %d', habit_id)
        day: HabitsCalendarSchema = HabitsCalendarSchema(
            habit_id=habit_id,
            date=str(date.today()),
            fulfillment=0
        )

        days = await self.habits_calendar_repository.get_by({'habit_id': day.habit_id, 'date': day.date})
        if len(days) != 0:
            logger.warning('Day, date: %s, already exists', day.date)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Day already exists')

        await self.habits_calendar_repository.create(day.model_dump())
        logger.info('Day by habit, id: %d, successfully created', habit_id)
