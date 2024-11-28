from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routing.auth import router_registration, router_auth, router_recovery, router_email_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_registration)
app.include_router(router_auth)
app.include_router(router_recovery)
app.include_router(router_email_code)
