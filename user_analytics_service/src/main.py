from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.analytics_rotes import analytics_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    '''Жизненный цикл приложения. Обновляет бд'''
    yield


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/analytics/openapi.json",
    docs_url="/api/analytics/docs"
    )


app.include_router(analytics_router, prefix='/api/analytics', tags=['analytics'])
