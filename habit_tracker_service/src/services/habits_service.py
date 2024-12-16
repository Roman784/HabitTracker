'''Сервис для работы с привычками'''


from fastapi import HTTPException, status
from typing import List

from src.services.base_habits_service import AbstractHabitsService
from src.repositories.base_repository import AbstractRepository
from src.schemas.habits_schemas import HabitCredsSchema, HabitSchema
from src.models.habits_model import HabitsModel
# from src.logging.habits_service_# logger import UsersService# logger


# logger = UsersService# logger().get_# logger()


class HabitsService(AbstractHabitsService):
    '''Сервис для работы с реальными привычками'''
    def __init__(self, habits_repository: AbstractRepository):
        self.habits_repository: AbstractRepository = habits_repository()


    async def create(self, data: HabitCredsSchema) -> int:
        '''Создаёт привычку и возвращает её id'''
        # logger.info('Creating new habit name: %s', data.name)

        habit_dict = data.model_dump()

        habits = await self.habits_repository.get_by({'name': data.name})
        if len(habits) != 0:
            # logger.warning('User name: %s already exists', data.name)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Habit already exists')

        habit_id = await self.habits_repository.create(habit_dict)
        # logger.info('User name: %s successfully created', data.name)
        return habit_id
    

    async def get_by_id(self, user_id: int, habit_id: int) -> HabitsModel:
        '''Возвращает данные привычки по id'''
        # logger.info('Retrieving the habit, id: %d', habit_id)
        habits = await self.habits_repository.get_by({'id': habit_id, 'user_id': user_id})

        if len(habits) == 0:
            # logger.warning('User id: %d not found', habit_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Habit not found')

        # logger.info('User id: %d successfully retrieved', habit_id)
        return habits[0]


    async def get_all(self, user_id: int) -> List[HabitsModel]:
        '''Возвращает все привычки'''
        habits = await self.habits_repository.get_by({'user_id': user_id})
        return habits


    async def update(self, user_id: int, habit_id: int, new_data: HabitCredsSchema):
        '''Обновляет данные привычки'''
        # logger.info('Updating the habit, id: %d', habit_id)

        habits = await self.habits_repository.get_by({'id': habit_id})

        if len(habits) == 0:
            # logger.warning('User id: %d not found', habit_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Habit not found')

        if habits[0].user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Habit of another user')

        habit_dict = new_data.model_dump()
        try:
            await self.habits_repository.update(habit_id, habit_dict)
            # logger.info('User id: %d successfully updated', habit_id)
        except ValueError as e:
            # logger.warning('User id: %d not found', habit_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


    async def delete(self, user_id: int, habit_id: int):
        '''Удаляет привычку'''
        # logger.info('Deleting the habit, id: %d', habit_id)

        habits = await self.habits_repository.get_by({'id': habit_id})

        if len(habits) == 0:
            # logger.warning('User id: %d not found', habit_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Habit not found')

        if habits[0].user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Habit of another user')

        try:
            await self.habits_repository.delete(habit_id)
            # logger.info('User id: %d successfully deleted', habit_id)
        except ValueError as e:
            # logger.warning('User id: %d not found', habit_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
