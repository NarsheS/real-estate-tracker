from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .database import Base


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