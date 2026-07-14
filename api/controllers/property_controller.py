from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import get_db, PropertyService
from ..schemas.property_schema import PropertyResponse
from ..schemas.price_history_schema import PriceHistoryResponse

router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


@router.get("/search", response_model=list[PropertyResponse])
def search_properties(
    city: str | None = None,
    state: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_area: float | None = None,
    max_area: float | None = None,
    db: Session = Depends(get_db)

):
    return PropertyService.search(
        db,
        city=city,
        state=state,
        min_price=min_price,
        max_price=max_price,
        min_area=min_area,
        max_area=max_area
    )

@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    return PropertyService.get_statistics(db)

@router.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    return PropertyService.get_cities(db)

@router.get("/states")
def get_states(db: Session = Depends(get_db)):
    return PropertyService.get_states(db)

@router.get("/{property_id}/history", response_model=list[PriceHistoryResponse])
def get_price_history(
    property_id: int,
    db: Session = Depends(get_db),
):
    return PropertyService.get_price_history(db, property_id)

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    return PropertyService.get_by_id(
        db,
        property_id
    )

@router.get("/", response_model=list[PropertyResponse])
def get_properties(db: Session = Depends(get_db)):
    return PropertyService.search(db)



