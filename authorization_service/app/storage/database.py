'''Создание и подключение к базе данных'''


from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.storage.models.base_model import BaseModel
from app.logging.logger_factory import get_database_logger


load_dotenv()
DATABASE_URL = getenv('DB_PATH')

logger = get_database_logger()


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
