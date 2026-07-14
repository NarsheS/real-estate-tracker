from api import UserAlert

from ..repositories.alert_repository import AlertRepository


def find_matching_alerts(
    db,
    city: str,
    price: float,
    area: float
):
    """
    Retorna todos os alertas que combinam com o imóvel.
    """

    alerts = (
        db.query(UserAlert)
        .filter(
            UserAlert.active == True
        )
        .all()
    )

    matches = []

    for alert in alerts:

        if alert.city.lower() != city.lower():
            continue

        if (
            alert.max_price is not None
            and price > alert.max_price
        ):
            continue

        if (
            alert.min_area is not None
            and area is not None
            and area < alert.min_area
        ):
            continue

        matches.append(alert)

    return matches


class AlertService:

    @staticmethod
    def create(db, data):
        alert = UserAlert(
            email=data.email,
            city=data.city,
            max_price=data.max_price,
            min_area=data.min_area,
            active=data.active
        )

        return AlertRepository.create(
            db,
            alert
        )


    @staticmethod
    def get_all(db):

        return AlertRepository.get_all(db)


    @staticmethod
    def get_by_id(
        db,
        alert_id: int
    ):

        return AlertRepository.get_by_id(
            db,
            alert_id
        )


    @staticmethod
    def update(
        db,
        alert_id: int,
        data
    ):

        alert = AlertRepository.get_by_id(
            db,
            alert_id
        )

        if alert is None:
            return None

        values = data.model_dump(
            exclude_unset=True
        )

        for key, value in values.items():
            setattr(
                alert,
                key,
                value
            )

        AlertRepository.save(db)

        return alert


    @staticmethod
    def delete(
        db,
        alert_id: int
    ):

        alert = AlertRepository.get_by_id(
            db,
            alert_id
        )

        if alert is None:
            return False

        AlertRepository.delete(
            db,
            alert
        )

        return True