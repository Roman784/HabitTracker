'''Схемы привычек'''


from pydantic import BaseModel
from datetime import date


class HabitAddSchema(BaseModel):
    filter_id: int
    name: str
    fulfillment: int
    color: str


class HabitCredsSchema(HabitAddSchema):
    '''Схема с реквезитами привычки'''
    user_id: int


class HabitSchema(HabitCredsSchema):
    '''Полная схема привычки'''
    id: int


class HabitsCalendarSchema(BaseModel):
    habit_id: int
    date: date
    fulfillment: int


class HabitsActivitySchema(BaseModel):
    date: date
    fulfillment: int
