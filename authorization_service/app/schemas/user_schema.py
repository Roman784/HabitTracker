'''Схема пользователя'''


from pydantic import BaseModel


class User(BaseModel):
    '''Схема пользователя'''
    username: str
    password: str

class UserResponse(User):
    '''Схема пользователя для выдачи'''
    id: int

class UserCreateResponse(BaseModel):
    '''Схема ответа при создании пользователя'''
    message: str
    user_id: int
