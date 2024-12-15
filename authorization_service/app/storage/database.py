'''Создание и подключение к базе данных'''


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.storage.models.base_model import BaseModel
from app.logging.logger_factory import get_database_logger
from app.configs.env_config import get_database_data


database_data = get_database_data()
logger = get_database_logger()


engine = create_async_engine(f'sqlite+aiosqlite:///{database_data['path']}')
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
