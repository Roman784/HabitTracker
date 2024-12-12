'''Создание базы данных и определение таблиц'''


from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


load_dotenv()
DATABASE_URL = getenv('DB_PATH')


engine = create_async_engine(f'sqlite+aiosqlite:///{DATABASE_URL}')
db_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class BaseTable(DeclarativeBase):
    '''База для всех таблиц'''
    pass

class UserTable(BaseTable):
    '''Таблица пользователя'''
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


async def create_tables():
    '''Создаёт таблицы'''
    print(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.create_all)

async def delete_tables():
    '''Удаляет таблицы'''
    async with engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.drop_all)
