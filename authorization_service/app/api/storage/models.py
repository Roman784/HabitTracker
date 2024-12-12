'''Модели'''


from pydantic import BaseModel


class User(BaseModel):
    '''Модель пользователя'''
    username: str
    password: str
