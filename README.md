# REAL-STATE-TRACKER
    Consulte docs.md para mais informações e detalhes sobre pastas, arquivos e endpoints.

## Instalação
    pip install -r requirements.txt

## Run api & swagger docs - Vai mostrar todos os endpints - OBS: ativar .venv primeiro
    .venv/scripts/activate.ps1
    uvicorn api.api_server:app --reload
    http://127.0.0.1:8000/docs