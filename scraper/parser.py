def parse_ad(ad: dict) -> dict:
    return {
        "id": ad.get("listId"),
        "title": ad.get("subject"),
        "price": ad.get("price"),
        "price_raw": ad.get("priceValue"),
        "location": ad.get("location"),
        "city": ad.get("locationDetails", {}).get("municipality"),
        "state": ad.get("locationDetails", {}).get("uf"),
        "image": (
            ad.get("images", [{}])[0].get("original")
            if ad.get("images")
            else None
        ),
        "url": ad.get("url"),
        "area": next(
            (
                p["value"]
                for p in ad.get("properties", [])
                if p["name"] == "size"
            ),
            None
        )
    }

def get_ads(data: dict) -> list:
    return (
        data
        .get("props", {})
        .get("pageProps", {})
        .get("ads", [])
    )