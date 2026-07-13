from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    email: str
    city: str
    max_price: float | None = None
    min_area: float | None = None
    active: bool = True


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    email: str | None = None
    city: str | None = None
    max_price: float | None = None
    min_area: float | None = None
    active: bool | None = None


class AlertResponse(AlertBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )