from datetime import datetime

from sqlalchemy import asc, desc

from api import Property


class PropertyRepository:

    # =====================================================
    # Busca por ID
    # =====================================================

    @staticmethod
    def get_by_id(db, property_id: int):
        return (
            db.query(Property)
            .filter(Property.id == property_id)
            .first()
        )

    @staticmethod
    def get_by_external_id(db, external_id: str):
        return (
            db.query(Property)
            .filter(Property.external_id == external_id)
            .first()
        )

    @staticmethod
    def exists(db, external_id: str):
        return (
            db.query(Property)
            .filter(Property.external_id == external_id)
            .first()
            is not None
        )

    # =====================================================
    # Create / Update / Delete
    # =====================================================

    @staticmethod
    def create(db, prop: Property):
        db.add(prop)
        db.flush()
        return prop

    @staticmethod
    def save(db):
        db.flush()

    @staticmethod
    def update(db, prop: Property, **kwargs):
        for key, value in kwargs.items():
            setattr(prop, key, value)

        db.flush()

        return prop

    @staticmethod
    def delete(db, prop: Property):
        db.delete(prop)

    # =====================================================
    # Search
    # =====================================================

    @staticmethod
    def search(
        db,

        id: int = None,
        external_id: str = None,

        city: str = None,
        state: str = None,
        source: str = None,

        title: str = None,
        url: str = None,

        min_price: float = None,
        max_price: float = None,

        min_area: float = None,
        max_area: float = None,

        active: bool = True,

        created_after: datetime = None,
        created_before: datetime = None,

        order_by: str = "created_at",
        descending: bool = False,

        limit: int = None,
        offset: int = None
    ):

        query = db.query(Property)

        # ------------------------------
        # Filtros
        # ------------------------------

        if id is not None:
            query = query.filter(Property.id == id)

        if external_id is not None:
            query = query.filter(
                Property.external_id == external_id
            )

        if city is not None:
            query = query.filter(
                Property.city == city
            )

        if state is not None:
            query = query.filter(
                Property.state == state
            )

        if source is not None:
            query = query.filter(
                Property.source == source
            )

        if title is not None:
            query = query.filter(
                Property.title.ilike(f"%{title}%")
            )

        if url is not None:
            query = query.filter(
                Property.url.ilike(f"%{url}%")
            )

        if min_price is not None:
            query = query.filter(
                Property.last_price >= min_price
            )

        if max_price is not None:
            query = query.filter(
                Property.last_price <= max_price
            )

        if min_area is not None:
            query = query.filter(
                Property.area >= min_area
            )

        if max_area is not None:
            query = query.filter(
                Property.area <= max_area
            )

        if active is not None:
            query = query.filter(
                Property.is_active == active
            )

        if created_after is not None:
            query = query.filter(
                Property.created_at >= created_after
            )

        if created_before is not None:
            query = query.filter(
                Property.created_at <= created_before
            )

        # ------------------------------
        # Ordenação
        # ------------------------------

        columns = {
            "id": Property.id,
            "price": Property.last_price,
            "area": Property.area,
            "title": Property.title,
            "city": Property.city,
            "state": Property.state,
            "created_at": Property.created_at,
            "last_seen": Property.last_seen_at,
        }

        if order_by not in columns:
            raise ValueError(
                f"Campo inválido para ordenação: {order_by}"
            )

        column = columns[order_by]

        query = query.order_by(
            desc(column) if descending else asc(column)
        )

        # ------------------------------
        # Paginação
        # ------------------------------

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        # IMPORTANTE:
        # retorna a Query, não a lista.
        return query

    # =====================================================
    # Utilitários
    # =====================================================

    @staticmethod
    def get_all(db):
        return (
            PropertyRepository
            .search(db)
            .all()
        )

    @staticmethod
    def count(db):
        return (
            db.query(Property)
            .count()
        )