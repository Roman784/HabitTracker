'''Модели привычек'''


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel
from src.schemas.habits_schemas import HabitSchema, HabitsCalendarSchema


class HabitsModel(BaseModel):
    '''Таблица привычек'''
    __tablename__ = 'habits'

    user_id: Mapped[int]
    filter_id: Mapped[int] # Область, к которой прычка принадлежит - спорт, учёба...
    name: Mapped[str]
    fulfillment: Mapped[int] # Желаемое количество выполнений раз в день. 
    color: Mapped[str]
    habits_calendar: Mapped[list['HabitsCalendarModel']] = relationship(
        'HabitsCalendarModel',
        back_populates='habit',
        cascade='all, delete-orphan'
    )

    def to_read_model(self) -> HabitSchema:
        '''str'''
        return HabitSchema(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            filter_id=self.filter_id,
            fulfillment=self.fulfillment,
            color=self.color
        )


class HabitsCalendarModel(BaseModel):
    '''Таблица календаря привычек'''
    __tablename__ = 'habits calendar'

    habit_id: Mapped[int] = mapped_column(ForeignKey('habits.id'), nullable=False)
    date: Mapped[str]
    fulfillment: Mapped[int]
    habit: Mapped[HabitsModel] = relationship('HabitsModel', back_populates='habits_calendar')

    def to_read_model(self) -> HabitsCalendarSchema:
        '''str'''
        return HabitsCalendarSchema(
            id=self.id,
            habit_id=self.habit_id,
            date=self.date,
            fulfillment=self.fulfillment,
        )
