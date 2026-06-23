from scraper import *
import json

url = "https://www.olx.com.br/imoveis/venda"

html = get_page(url)

data = get_next_data(html)

ads = get_ads(data)

parsed = [parse_ad(ad) for ad in ads]

print(json.dumps(parsed, indent=2, ensure_ascii=False))