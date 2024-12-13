'''Точка входа в сервис авторизации'''


from contextlib import asynccontextmanager
from typing import Annotated, Tuple
from fastapi import FastAPI, Depends
from .schemas.user_schema import User
from .storage.repositories.user_repository import UserRepository
from .storage.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/create')
async def create(user_data: Annotated[User, Depends()]):
    await UserRepository.create(user_data)

@app.get('/read', response_model=Tuple[int, User])
async def get(user_id: int):
    user = await UserRepository.read(user_id)
    return (user.id, user)

@app.put('/update')
async def update(user_id: int, user_data: Annotated[User, Depends()]):
    await UserRepository.update(user_id, user_data)

@app.delete('/delete')
async def delete(user_id: int):
    await UserRepository.delete(user_id)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
