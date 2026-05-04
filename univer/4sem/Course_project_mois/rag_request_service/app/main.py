from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI(
    title="RAG Request Processing Service",
    description="Модуль обработки входящего запроса для справочной RAG-системы",
    version="0.1.0",
)

app.include_router(router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")