'''Схемы привычек'''


from pydantic import BaseModel


class HabitsCredsSchema(BaseModel):
    '''Схема с реквезитами пользователя'''
    user_id: int
    filter_id: int
    name: str
    fulfillment: int
    rate: int
    color: str

class HabitsSchema(HabitsCredsSchema):
    '''Полная схема пользователя'''
    id: int
