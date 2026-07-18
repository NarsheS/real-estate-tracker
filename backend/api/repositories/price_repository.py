from api import PriceHistory


class PriceRepository:

    @staticmethod
    def create(
        db,
        property_id: int,
        price: float
    ):

        history = PriceHistory(
            property_id=property_id,
            price=price
        )

        db.add(history)

        return history