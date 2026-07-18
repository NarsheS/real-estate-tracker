from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String
)

from sqlalchemy.orm import relationship

from .database import Base


# ==========================================================
# Imóveis
# ==========================================================

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)

    source = Column(
        String,
        nullable=False
    )

    external_id = Column(
        String,
        unique=True,
        nullable=False
    )

    title = Column(String)

    city = Column(String)

    state = Column(String)

    image = Column(String)

    url = Column(String)

    area = Column(Float)

    # preço atual do anúncio
    last_price = Column(Float)

    # última vez que o scraper encontrou este anúncio
    last_seen_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # última alteração feita neste registro
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # anúncio ainda existe?
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    # quando entrou no sistema
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    prices = relationship(
        "PriceHistory",
        back_populates="property",
        cascade="all, delete-orphan"
    )


# ==========================================================
# Histórico de preços
# ==========================================================

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(
        Integer,
        primary_key=True
    )

    property_id = Column(
        Integer,
        ForeignKey("properties.id"),
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    captured_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    property = relationship(
        "Property",
        back_populates="prices"
    )


# ==========================================================
# Alertas
# ==========================================================

class UserAlert(Base):
    __tablename__ = "user_alerts"

    id = Column(
        Integer,
        primary_key=True
    )

    email = Column(
        String,
        nullable=False
    )

    city = Column(
        String,
        nullable=False
    )

    max_price = Column(Float)

    min_area = Column(Float)

    active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )