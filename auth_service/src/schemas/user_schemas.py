'''Схемы пользователей'''


from pydantic import BaseModel


class UserCredsSchema(BaseModel):
    '''Схема с реквезитами пользователя'''
    name: str
    password: str

class UserSchema(UserCredsSchema):
    '''Полная схема пользователя'''
    id: int
