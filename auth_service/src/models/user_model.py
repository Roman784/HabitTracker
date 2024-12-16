'''Модель пользователя'''


from sqlalchemy.orm import Mapped, mapped_column
from .base_model import BaseModel
from src.schemas.user_schemas import UserSchema


class UserModel(BaseModel):
    '''Таблица пользователя'''
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def to_read_model(self) -> UserSchema:
        '''str'''
        return UserSchema(
            id=self.id,
            name=self.name,
            password=self.password
        )
