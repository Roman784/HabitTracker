from contextlib import asynccontextmanager
from fastapi import FastAPI
from pika import BlockingConnection, ConnectionParameters
import threading


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    # thread = threading.Thread(target=main)
    # thread.start()
    yield


app = FastAPI(lifespan=lifespan)
