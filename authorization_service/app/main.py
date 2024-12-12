'''Точка входа в сервис авторизации'''


from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from api.storage.storage import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
