from fastapi import FastAPI
from src.routing.auth import router as registration_router

app = FastAPI()

app.include_router(registration_router)