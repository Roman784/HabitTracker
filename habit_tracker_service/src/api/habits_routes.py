'''Конечные точки для работы с привычками'''


from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.services.base_habits_service import AbstractHabitsService
from src.schemas.habits_schemas import HabitCredsSchema, HabitAddSchema
from src.api.dependencies import habits_service
from src.api.dependencies import get_payload_token


habits_router = APIRouter()


@habits_router.put('/mark', status_code=status.HTTP_200_OK)
async def mark_fulfillment(
    habit_id: int,
    habits_service: Annotated[AbstractHabitsService, Depends(habits_service)],
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Отмечает выполнение привычки'''
    user_id = payload['id']
    day_fulfillment, habit_fulfillment = await habits_service.mark_fulfillment(user_id, habit_id)
    return { 
        'message': 'Habit marked',
        'day_fulfillment': day_fulfillment,
        'habit_fulfillment': habit_fulfillment
    }


@habits_router.get('/get-habits', status_code=status.HTTP_200_OK)
async def get_all(
    habits_service: Annotated[AbstractHabitsService, Depends(habits_service)],
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Возвращает данные пользователя по id'''
    user_id = payload['id']
    habits = await habits_service.get_all(user_id)
    return {'habits': habits}


@habits_router.get('/get', status_code=status.HTTP_200_OK)
async def get(
    habit_id: int,
    habits_service: Annotated[AbstractHabitsService, Depends(habits_service)],
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Возвращает данные привычки по id'''
    user_id = payload['id']
    habit = await habits_service.get_by_id(user_id, habit_id)
    return {'habit': habit}


@habits_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(
    data: Annotated[HabitAddSchema, Depends()],
    habits_service: Annotated[AbstractHabitsService, Depends(habits_service)],
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Создаёт привычку'''
    user_id = payload['id']
    data = data.model_dump()
    data['user_id'] = user_id
    habit_data = HabitCredsSchema(**data)

    habit_id = await habits_service.create(habit_data)
    return { 'habit_id': habit_id }


@habits_router.put('/update', status_code=status.HTTP_200_OK)
async def update(
    habit_id: int,
    new_data: Annotated[HabitAddSchema, Depends()],
    habits_service: Annotated[AbstractHabitsService, Depends(habits_service)],
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Обновляет данные привычки'''
    user_id = payload['id']
    await habits_service.update(user_id, habit_id, new_data)
    return { 'message': 'Habit updated' }


@habits_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete(
    habit_id: int,
    habits_service: Annotated[AbstractHabitsService, Depends(habits_service)],
    payload: Annotated[any, Depends(get_payload_token)]
):
    '''Удаляет пользователя'''
    user_id = payload['id']
    await habits_service.delete(user_id, habit_id)
    return { 'message': 'Habit deleted' }
