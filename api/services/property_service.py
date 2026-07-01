from datetime import datetime, timezone

from api import Property

from utils import compare_price

from .alerts_service import find_matching_alerts

from ..repositories.property_repository import PropertyRepository
from ..repositories.price_repository import PriceRepository


class PropertyService:

    # ==========================================================
    # CRUD
    # ==========================================================

    @staticmethod
    def get_by_id(db, property_id: int):
        return PropertyRepository.get_by_id(
            db,
            property_id
        )

    @staticmethod
    def search(db, **filters):
        return PropertyRepository.search(
            db,
            **filters
        )

    @staticmethod
    def create(db, data: dict):

        prop = Property(**data)

        return PropertyRepository.create(
            db,
            prop
        )

    @staticmethod
    def update(db, prop: Property, **data):

        for key, value in data.items():
            setattr(prop, key, value)

        PropertyRepository.save(db)

        return prop

    @staticmethod
    def delete(db, prop: Property):

        PropertyRepository.delete(
            db,
            prop
        )

    @staticmethod
    def count(db):

        return PropertyRepository.count(db)

    # ==========================================================
    # Marca imóveis que desapareceram
    # ==========================================================

    @staticmethod
    def mark_missing_as_inactive(
        db,
        found_external_ids: set
    ):

        properties = PropertyRepository.get_all(db)

        for prop in properties:

            if prop.external_id not in found_external_ids:

                prop.is_active = False

        PropertyRepository.save(db)

    # ==========================================================
    # Processa um anúncio do scraper
    # ==========================================================

    @staticmethod
    def process_ad(db, ad: dict):

        new_price = ad["price_raw"]

        if new_price is None:
            return None

        external_id = str(ad["id"])

        prop = PropertyRepository.get_by_external_id(
            db,
            external_id
        )

        # ------------------------------------------------------
        # Novo imóvel
        # ------------------------------------------------------

        if prop is None:

            prop = Property(

                source="OLX",

                external_id=external_id,

                title=ad["title"],

                city=ad["city"],

                state=ad["state"],

                image=ad["image"],

                url=ad["url"],

                area=ad["area"],

                last_price=new_price,

                last_seen_at=datetime.now(
                    timezone.utc
                ),

                is_active=True

            )

            PropertyRepository.create(
                db,
                prop
            )

            PriceRepository.create(
                db,
                prop.id,
                new_price
            )

            comparison = None

        # ------------------------------------------------------
        # Imóvel existente
        # ------------------------------------------------------

        else:

            comparison = compare_price(
                prop.last_price,
                new_price
            )

            if (
                comparison is not None
                and comparison["status"] != "same"
            ):

                PriceRepository.create(
                    db,
                    prop.id,
                    new_price
                )

            prop.last_price = new_price
            prop.last_seen_at = datetime.now(
                timezone.utc
            )
            prop.is_active = True

            PropertyRepository.save(db)

        # ------------------------------------------------------
        # Busca alertas
        # ------------------------------------------------------

        alerts = find_matching_alerts(

            db,

            prop.city,

            new_price,

            prop.area

        )

        return {

            "property": prop,

            "comparison": comparison,

            "alerts": alerts

        }