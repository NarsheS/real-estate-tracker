from api import UserAlert

# Alerta o usuário via email caso algum dado bata o requisito
def find_matching_alerts(
    db,
    city: str,
    price: float,
    area: float
):
    alerts = (
        db.query(UserAlert)
        .filter(
            UserAlert.active == True
        )
        .all()
    )

    matches = []

    for alert in alerts:

        if alert.city != city:
            continue

        if price > alert.max_price:
            continue

        # Se o usuário definiu área mínima
        if (
            alert.min_area is not None
            and area is not None
            and area < alert.min_area
        ):
            continue

        matches.append(alert)

    return matches