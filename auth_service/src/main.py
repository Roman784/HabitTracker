'''Точка входа в сервис авторизации'''


from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.databse.database import create_tables, delete_tables
from src.api.auth_routes import auth_router
from src.api.crud_routes import crud_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router, prefix='/api/auth', tags=['auth'])
app.include_router(crud_router, prefix='/api/crud', tags=['crud'])
