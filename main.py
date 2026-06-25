from scraper import get_page, get_next_data
from utils import get_ads, parse_ad
from services import compare_price, find_matching_alerts
from api import Base, engine, SessionLocal, Property, PriceHistory

# Conecta com o banco de dados
Base.metadata.create_all(bind=engine)
db = SessionLocal()

url = "https://www.olx.com.br/imoveis/venda"

# Acessa a página simulando um usuário no navegador
html = get_page(url) 

# Obtém os dados dentro da html, em um script de id __NEXT_DATA__
data = get_next_data(html)

# Obtém o alvo (anúncios) dentro do script
ads = get_ads(data)

# Formatando os dados para json
parsed = [parse_ad(ad) for ad in ads]


# Tenta adicionar toda a informação do scrapper ao banco de dados
for ad in parsed:

    property = (
        db.query(Property)
        .filter(
            Property.external_id == str(ad["id"])
        )
        .first()
    )

    if property is None:

        property = Property(
            source="OLX",
            external_id=str(ad["id"]),
            title=ad["title"],
            city=ad["city"],
            state=ad["state"],
            image=ad["image"],
            url=ad["url"],
            area=ad["area"]
        )

        db.add(property)
        db.flush()

    new_price = ad["price_raw"]

    if new_price is None:
        continue

    comparison = compare_price(
        db,
        property.id,
        new_price
    )

    if comparison:

        if comparison["status"] == "down":

            print("=" * 60)
            print("🔥 PREÇO CAIU")
            print(property.title)
            print(
                f"De R$ {comparison['old_price']:,.2f}"
            )
            print(
                f"Para R$ {comparison['new_price']:,.2f}"
            )
            print(
                f"{comparison['percent']:.2f}%"
            )
            print("=" * 60)

        elif comparison["status"] == "up":

            print("=" * 60)
            print("📈 PREÇO SUBIU")
            print(property.title)
            print("=" * 60)
            
        # OPCIONAL
        elif comparison["status"] == "same":

            print("=" * 60)
            print("📈 PREÇO NÃO MUDOU")
            print(property.title)
            print("=" * 60)

    history = PriceHistory(
        property_id=property.id,
        price=new_price
    )

    db.add(history)

    matches = find_matching_alerts(
        db,
        property.city,
        new_price,
        property.area
    )

    for alert in matches:

        print("=" * 60)
        print(f"🔔 ALERTA PARA {alert.email}")
        print(property.title)
        print(f"Cidade: {property.city}")
        print(f"Preço: R$ {new_price:,.2f}")
        print(property.url)
        print("=" * 60)

db.commit()