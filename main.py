from scraper import ScraperService

from api import (
    Base,
    engine,
    SessionLocal
)


# ==========================================================
# Inicialização
# ==========================================================

Base.metadata.create_all(bind=engine)

db = SessionLocal()

ScraperService.run(db)

db.commit()

db.close()