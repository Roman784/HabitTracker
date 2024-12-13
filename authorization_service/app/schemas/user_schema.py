'''Схема пользователя'''


from pydantic import BaseModel


class User(BaseModel):
    '''Схема пользователя'''
    username: str
    password: str
