from fastapi import FastAPI

from api.controllers.property_controller import router as property_router
from api.controllers.alert_controller import router as alert_router


app = FastAPI(
    title="Real Estate Tracker",
    version="0.1.4"
)

app.include_router(property_router)
app.include_router(alert_router)