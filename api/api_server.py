from fastapi import FastAPI

from api import router as property_router

app = FastAPI(
    title="Real Estate Tracker",
    version="0.1.3"
)

app.include_router(property_router)