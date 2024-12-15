'''Создание и подключение к базе данных'''


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.models.base_model import BaseModel


engine = create_async_engine(f'sqlite+aiosqlite:///users.sqlite')
db_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables():
    '''Создаёт таблицы'''
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def delete_tables():
    '''Удаляет таблицы'''
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
