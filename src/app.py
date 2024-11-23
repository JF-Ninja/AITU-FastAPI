from fastapi import FastAPI
from AITU_Project.src.routing.auth import router as registration_router

app = FastAPI(openapi_url="/core/openapi.json", docs_url="/core/docs")
app.include_router(registration_router)