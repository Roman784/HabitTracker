'''Схемы привычек'''


from pydantic import BaseModel


class HabitAddSchema(BaseModel):
    filter_id: int
    name: str
    fulfillment: int
    rate: int
    color: str


class HabitCredsSchema(HabitAddSchema):
    '''Схема с реквезитами привычки'''
    user_id: int


class HabitSchema(HabitCredsSchema):
    '''Полная схема привычки'''
    id: int
