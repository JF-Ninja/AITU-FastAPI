from fastapi import FastAPI
from routing.auth import router as registration_router

app = FastAPI()

app.include_router(registration_router)