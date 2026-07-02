from .database import Base, engine, SessionLocal
from .models import Property, PriceHistory, UserAlert
from .services.alerts_service import find_matching_alerts
from .services.property_service import PropertyService
from .repositories.property_repository import PropertyRepository
from .dependencies import get_db
from .controllers.property_controller import router