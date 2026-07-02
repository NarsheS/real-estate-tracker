from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PriceHistoryResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    price: float

    captured_at: datetime