'''Базовая модель'''


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    '''База для всех таблиц'''
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
