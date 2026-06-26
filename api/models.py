from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .database import Base

# Registrar propriedades
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)

    source = Column(String)
    external_id = Column(String, unique=True)

    title = Column(String)
    city = Column(String)
    state = Column(String)

    image = Column(String)

    url = Column(String)

    area = Column(Float)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    prices = relationship(
        "PriceHistory",
        back_populates="property"
    )

# Registrar preços
class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id")
    )

    price = Column(Float)

    captured_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    property = relationship(
        "Property",
        back_populates="prices"
    )

# Para criar alertas
class UserAlert(Base):
    __tablename__ = "user_alerts"

    id = Column(
        Integer,
        primary_key=True
    )

    city = Column(String)

    max_price = Column(Float)

    min_area = Column(Float)

    email = Column(String, nullable=False)

    active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        datetime,
        default=lambda: datetime.now(timezone.utc)
    )