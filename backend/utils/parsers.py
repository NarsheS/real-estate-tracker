import re


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


def extract_area(details):
    for key, value in details.items():

        if "metros quadrados" in key:
            return parse_area(value)

    return None


def extract_id(url):
    if not url:
        return None

    match = re.search(
        r"-(\d+)$",
        url
    )

    return match.group(1) if match else url


def parse_location(location):
    if not location or "-" not in location:
        return None, None

    city, state = location.split("-", 1)

    return (
        city.strip(),
        state.strip()
    )


def parse_ad(ad: dict) -> dict:
    details = ad.get(
        "details",
        {}
    )

    city, state = parse_location(
        ad.get("location")
    )


    return {
        "source": "olx",

        "id": extract_id(
            ad.get("url")
        ),

        "title": ad.get(
            "title"
        ),

        "price": parse_price(
            ad.get("price")
        ),

        "price_raw": ad.get(
            "price"
        ),

        "location": ad.get(
            "location"
        ),

        "city": city,

        "state": state,

        "image": ad.get(
            "image"
        ),

        "url": ad.get(
            "url"
        ),

        "area": extract_area(
            details
        )
    }