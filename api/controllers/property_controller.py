from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import get_db
from api import PropertyService

router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


@router.get("/")
def get_properties(db: Session = Depends(get_db)):
    return PropertyService.search(db)

@router.get("/{property_id}")
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    return PropertyService.get_by_id(
        db,
        property_id
    )

@router.get("/search")
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