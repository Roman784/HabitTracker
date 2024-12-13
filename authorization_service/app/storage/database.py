'''Создание и подключение к базе данных'''


import logging
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models.base_model import BaseModel


load_dotenv()
DATABASE_URL = getenv('DB_PATH')
LOGS_FILE_NAME = getenv('DATABASE_LOGS_FILE')

logging.basicConfig(
    filename=LOGS_FILE_NAME,
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger('database')


engine = create_async_engine(f'sqlite+aiosqlite:///{DATABASE_URL}')
db_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables():
    '''Создаёт таблицы'''
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        logger.info("Database created")

async def delete_tables():
    '''Удаляет таблицы'''
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        logger.info("Database deleted")
