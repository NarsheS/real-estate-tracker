from api import PriceHistory

def check_price_change(db, property_id: int, new_price: float):
    """
    Retorna:
    - "caiu"
    - "subiu"
    - "manteve"
    - None (primeiro preço)
    """

    last_price = (
        db.query(PriceHistory)
        .filter(
            PriceHistory.property_id == property_id
        )
        .order_by(
            PriceHistory.captured_at.desc()
        )
        .first()
    )

    if not last_price:
        return None
    
    if new_price < last_price:
        return "caiu"
    
    if new_price > last_price:
        return "subiu"
    
    return "same"

def get_price_change(db, property_id: int, new_price: float):

    last_price = (
        db.query(PriceHistory)
        .filter(
            PriceHistory.property_id == property_id
        )
        .order_by(
            PriceHistory.captured_at.desc()
        )
        .first()
    )

    if not last_price:
        return None
    
    difference = new_price - last_price.price

    percent = (difference / last_price.price) * 100

    return {
        "old_price": last_price.price,
        "new_price": new_price,
        "difference": difference,
        "percent": percent
    }