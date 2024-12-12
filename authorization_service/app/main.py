'''Точка входа в сервис авторизации'''


from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.storage.storage import UserTable, create_tables, delete_tables
from app.api.storage.repository import UserRepository
from app.api.storage.models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/create')
async def create(user_data: User):
    await UserRepository.create(user_data)

@app.get('/read')
async def get(user_id: int):
    user = await UserRepository.read(user_id)
    return user

@app.put('/update')
async def update(user_id: int, user_data: User):
    await UserRepository.update(user_id, user_data)

@app.delete('/delete')
async def delete(user_id: int):
    await UserRepository.delete(user_id)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
