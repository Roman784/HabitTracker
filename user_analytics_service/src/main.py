from contextlib import asynccontextmanager
from fastapi import FastAPI
# from pika import BlockingConnection, ConnectionParameters
# import threading

from src.api.analytics_rotes import analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    # thread = threading.Thread(target=main)
    # thread.start()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(analytics_router, prefix='/api/analytics', tags=['analytics'])
