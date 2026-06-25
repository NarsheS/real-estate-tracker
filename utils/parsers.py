def get_ads(data: dict) -> list:
    return (
        data
        .get("props", {})
        .get("pageProps", {})
        .get("ads", [])
    )

def parse_price(price: str) -> float:
    if not price:
        return None
    
    return float(
        price
        .replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )

def parse_area(area: str) -> float:

    if not area:
        return None

    return float(
        area
        .replace("m²", "")
        .replace(",", ".")
        .strip()
    )

def parse_ad(ad: dict) -> dict:
    return {
        "id": ad.get("listId"),
        "title": ad.get("subject"),
        "price": parse_price(
            ad.get("price")
        ),
        "price_raw": parse_price(
            ad.get("priceValue")
        ),
        "location": ad.get("location"),
        "city": ad.get("locationDetails", {}).get("municipality"),
        "state": ad.get("locationDetails", {}).get("uf"),
        "image": (
            ad.get("images", [{}])[0].get("original")
            if ad.get("images")
            else None
        ),
        "url": ad.get("url"),
        "area": parse_area(
            next(
            (
                p["value"]
                for p in ad.get("properties", [])
                if p["name"] == "size"
            ),
            None
        )
        )
    }