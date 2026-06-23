from scraper import *
import json

from api import Base, engine, Property, PriceHistory

Base.metadata.create_all(bind=engine)

url = "https://www.olx.com.br/imoveis/venda"

# Acessa a página simulando um usuário no navegador
html = get_page(url) 

# Obtém os dados dentro da html, em um script de id __NEXT_DATA__
data = get_next_data(html)

# Obtém o alvo (anúncios) dentro do script
ads = get_ads(data)

# Formatando os dados para json
parsed = [parse_ad(ad) for ad in ads]

print(json.dumps(parsed, indent=2, ensure_ascii=False))