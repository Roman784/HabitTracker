'''Точка входа в сервис авторизации'''


from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.databse.database import create_tables
from src.api.auth_routes import auth_router
from src.api.crud_routes import crud_router
from src.message_broker.message_brokers import connect_brokers, start_consuming, close_brokers


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
    openapi_url="/api/auth/openapi.json",
    docs_url="/api/auth/docs"
    )


app.include_router(auth_router, prefix='/api/auth', tags=['auth'])
app.include_router(crud_router, prefix='/api/auth/crud', tags=['crud'])
