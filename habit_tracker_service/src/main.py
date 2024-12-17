'''Точка входа в сервис по работе с привычками'''


from contextlib import asynccontextmanager
from fastapi import FastAPI
import threading

from src.database.database import create_tables, delete_tables
from src.api.habits_routes import habits_router
from src.message_broker.message_brokers import connect_brokers, close_brokers, start_consuming


@asynccontextmanager
async def lifespan(_: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    # await delete_tables()
    await create_tables()
    await connect_brokers()
    await start_consuming()
    yield
    await close_brokers()


app = FastAPI(lifespan=lifespan)


app.include_router(habits_router, prefix='/api/habits', tags=['habits'])
