'''Точка входа в сервис по работе с привычками'''


from contextlib import asynccontextmanager
from fastapi import FastAPI
import threading

from src.database.database import create_tables, delete_tables
from src.api.habits_routes import habits_router
from src.api.rabbitmq_api import get_request


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    thread = threading.Thread(target=get_request)
    thread.start()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(habits_router, prefix='/api/habits', tags=['habits'])
