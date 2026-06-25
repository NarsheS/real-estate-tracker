from scraper import get_page, get_next_data
from utils import get_ads, parse_ad
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
    # Checa se ja existe X property para evitar erros
    property = (
        db.query(Property)
        .filter(
            Property.external_id == str(ad["id"])
        )
        .first()
    )

    # Se não tiver X property, adiciona ao banco
    if not property:

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

    # Adiciona o no preço ao banco
    history = PriceHistory(
        property_id=property.id,
        price=ad["price_raw"]
    )

    db.add(history)

db.commit()