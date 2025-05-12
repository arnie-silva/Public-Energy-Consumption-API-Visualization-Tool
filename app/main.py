from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Public Energy Consumption")
app.include_router(router)