from api import UserAlert


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