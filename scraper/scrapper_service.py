from scraper import get_page, get_next_data
from utils import get_ads, parse_ad

from api import (
    PropertyService,
    PropertyRepository
)

class ScraperService:

    @staticmethod
    def run(db):
        url = "https://www.olx.com.br/imoveis/venda"

        html = get_page(url)

        data = get_next_data(html)

        ads = get_ads(data)

        parsed = [parse_ad(ad) for ad in ads]

        found_properties = set()

        # ==========================================================
        # Processa todos os anúncios
        # ==========================================================

        for ad in parsed:

            result = PropertyService.process_ad(
                db,
                ad
            )

            if result is None:
                continue

            prop = result["property"]
            comparison = result["comparison"]
            alerts = result["alerts"]

            found_properties.add(
                prop.external_id
            )

            # ======================================================
            # Alteração de preço
            # ======================================================

            if comparison:

                if comparison["status"] == "down":

                    print("=" * 60)
                    print("🔥 PREÇO CAIU")
                    print(prop.title)
                    print(
                        f"De R$ {comparison['old_price']:,.2f}"
                    )
                    print(
                        f"Para R$ {comparison['new_price']:,.2f}"
                    )
                    print(
                        f"Variação: {comparison['percent']:.2f}%"
                    )
                    print("=" * 60)

                elif comparison["status"] == "up":

                    print("=" * 60)
                    print("📈 PREÇO SUBIU")
                    print(prop.title)
                    print(
                        f"De R$ {comparison['old_price']:,.2f}"
                    )
                    print(
                        f"Para R$ {comparison['new_price']:,.2f}"
                    )
                    print(
                        f"Variação: {comparison['percent']:.2f}%"
                    )
                    print("=" * 60)

            # ======================================================
            # Alertas
            # ======================================================

            for alert in alerts:

                print("=" * 60)
                print(f"🔔 ALERTA PARA {alert.email}")
                print(prop.title)
                print(f"Cidade: {prop.city}")
                print(f"Preço: R$ {prop.last_price:,.2f}")
                print(prop.url)
                print("=" * 60)

        # ==========================================================
        # Marca anúncios removidos
        # ==========================================================

        for prop in PropertyRepository.get_all(db):

            if prop.external_id not in found_properties:

                prop.is_active = False

        PropertyRepository.save(db)