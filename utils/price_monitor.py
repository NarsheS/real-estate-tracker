def compare_price(
    old_price: float | None,
    new_price: float
) -> dict | None:
    """
    Compara o preço antigo com o novo.

    Retorna:
        None -> primeiro preço

        {
            status,
            old_price,
            new_price,
            difference,
            percent
        }
    """

    if old_price is None:
        return None

    difference = new_price - old_price

    if old_price == 0:
        percent = 0
    else:
        percent = (difference / old_price) * 100

    if difference < 0:
        status = "down"
    elif difference > 0:
        status = "up"
    else:
        status = "same"

    return {
        "status": status,
        "old_price": old_price,
        "new_price": new_price,
        "difference": difference,
        "percent": percent,
    }