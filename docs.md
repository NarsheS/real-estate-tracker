# Introdução
    O objetivo desse software é obter informações sobre os valores dos imovéis e guardar em um banco de 
dados, para posteriormente, comparar os preços e apresentar um gráfico sobre o mercado de imóveis da região desejada. Os valores serão documentados diariamente, podendo ser usado para pesquisas ou ate mesmo uma "previsão" de preço. Os usuários poderão pedir para o software emitir um alerta caso X imóvel esteja abaixo de Y valor.

# Scraper
    Tem como função obter os dados do alvo solicidado, no caso deste software, um site de imobiliário do
qual encontrei uma "vunerabilidade".

## client.py
    Acessa o alvo enquanto simula ser uma usuário comum no navegador, sem isso, recebemos um erro do alvo 
que nos impede de acessar.

## extractor.py
    Extrai as informações de um script dentro do html.

## parser.py
    Formata os dados extraídos para json.