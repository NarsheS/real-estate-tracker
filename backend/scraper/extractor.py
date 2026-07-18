from bs4 import BeautifulSoup


def extract_ads(html):
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    ads = []

    cards = soup.select(
        "section.olx-adcard"
    )


    for card in cards:

        title = card.select_one(
            ".olx-adcard__title"
        )

        price = card.select_one(
            ".olx-adcard__price"
        )

        link = card.select_one(
            ".olx-adcard__link"
        )

        location = card.select_one(
            ".olx-adcard__location"
        )

        image = card.select_one(
            ".olx-adcard__media img"
        )


        details = {}

        for detail in card.select(
            ".olx-adcard__detail"
        ):

            key = detail.get(
                "aria-label"
            )

            value = detail.get_text(
                strip=True
            )

            details[key] = value


        ads.append(
            {
                "title": (
                    title.get_text(strip=True)
                    if title
                    else None
                ),

                "price": (
                    price.get_text(strip=True)
                    if price
                    else None
                ),

                "url": (
                    link["href"]
                    if link
                    else None
                ),

                "location": (
                    location.get_text(strip=True)
                    if location
                    else None
                ),

                "image": (
                    image.get("src")
                    if image
                    else None
                ),

                "details": details
            }
        )


    return ads