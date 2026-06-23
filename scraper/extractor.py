from bs4 import BeautifulSoup
import json

def get_next_data(html: str) -> dict:
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    script = soup.find(
        "script",
        id="__NEXT_DATA__"
    )

    if not script:
        raise Exception(
            "__NEXT_DATA__ não encontrado"
        )
    
    return json.loads(script.text)