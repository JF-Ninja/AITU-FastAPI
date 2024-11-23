print(1)
from fastapi import FastAPI
from src.routing.auth import router as registration_router
print(2)
app = FastAPI()

app.include_router(registration_router)