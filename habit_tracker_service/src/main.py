'''Точка входа в сервис по работе с привычками'''


from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database.database import create_tables, delete_tables
from src.api.habits_routes import habits_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(habits_router, prefix='/api/habits', tags=['habits'])
