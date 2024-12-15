'''Точка входа в сервис авторизации'''


from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.storage.database import create_tables, delete_tables
from app.routers.crud_router import crud_router
from app.routers.auth_router import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix='/api/auth', tags=['auth'])
app.include_router(crud_router, prefix='/api/crud', tags=['crud'])
