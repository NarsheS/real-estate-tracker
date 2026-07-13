from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from api import (
    get_db,
    AlertService
)

from api.schemas.alert_schema import (
    AlertCreate,
    AlertUpdate,
    AlertResponse
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.post("/", response_model=AlertResponse)
def create_alert(
    data: AlertCreate,
    db: Session = Depends(get_db)
):
    return AlertService.create(
        db,
        data
    )


@router.get("/", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return AlertService.get_all(db)


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = AlertService.get_by_id(
        db,
        alert_id
    )

    if alert is None:
        raise HTTPException(
            404,
            "Alert not found"
        )

    return alert


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    data: AlertUpdate,
    db: Session = Depends(get_db)
):
    alert = AlertService.update(
        db,
        alert_id,
        data
    )

    if alert is None:
        raise HTTPException(
            404,
            "Alert not found"
        )

    return alert


@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    deleted = AlertService.delete(
        db,
        alert_id
    )

    if not deleted:
        raise HTTPException(
            404,
            "Alert not found"
        )

    return {
        "message": "Alert deleted successfully"
    }