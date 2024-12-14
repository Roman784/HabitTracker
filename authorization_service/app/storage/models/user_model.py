'''Модель пользователя'''


from sqlalchemy.orm import Mapped, mapped_column
from app.storage.models.base_model import BaseModel


class UserModel(BaseModel):
    '''Таблица пользователя'''
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
