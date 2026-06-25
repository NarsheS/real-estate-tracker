from api import PriceHistory


def compare_price(db, property_id: int, new_price: float):
    """
    Compara o novo preço com o último registrado.

    Retorna:
        None -> primeiro preço do imóvel

        {
            "status": "down" | "up" | "same",
            "old_price": float,
            "new_price": float,
            "difference": float,
            "percent": float
        }
    """

    last = (
        db.query(PriceHistory)
        .filter(
            PriceHistory.property_id == property_id
        )
        .order_by(
            PriceHistory.captured_at.desc()
        )
        .first()
    )

    if last is None:
        return None

    difference = new_price - last.price

    percent = (
        difference / last.price
    ) * 100

    if difference < 0:
        status = "down"

    elif difference > 0:
        status = "up"

    else:
        status = "same"

    return {
        "status": status,
        "old_price": last.price,
        "new_price": new_price,
        "difference": difference,
        "percent": percent
    }