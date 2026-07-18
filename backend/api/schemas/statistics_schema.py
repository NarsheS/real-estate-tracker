from pydantic import BaseModel

class PropertyStatisticsResponse(BaseModel):
    total: int
    active: int
    inactive: int
    active_percentage: float
    inactive_percentage: float
    cities: int
    states: int