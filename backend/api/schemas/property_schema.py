from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .price_history_schema import PriceHistoryResponse


class PropertyResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    source: str
    external_id: str
    title: str | None
    city: str |None
    state: str | None
    image: str | None
    url: str | None
    area: float | None
    last_price: float | None
    last_seen_at: datetime
    updated_at: datetime
    is_active: bool
    created_at: datetime
    prices: list[PriceHistoryResponse] = []