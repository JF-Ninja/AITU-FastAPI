from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routing.auth import router, router1, router2, router3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(router1)
app.include_router(router2)
app.include_router(router3)
