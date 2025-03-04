'''Точка входа в сервис по работе с привычками'''


from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database.database import create_tables
from src.api.habits_routes import habits_router
from src.message_broker.message_brokers import connect_brokers, close_brokers, start_consuming


@asynccontextmanager
async def lifespan(_: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await create_tables()
    await connect_brokers()
    await start_consuming()
    yield
    await close_brokers()


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/habits/openapi.json",
    docs_url="/api/habits/docs"
    )


app.include_router(habits_router, prefix='/api/habits', tags=['habits'])
