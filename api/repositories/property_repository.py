from api import Property
from sqlalchemy import asc, desc
from datetime import datetime


class PropertyRepository:
    # ---------------------------------------
    # Busca por ID
    # ---------------------------------------

    @staticmethod
    def get_by_id(db, property_id: int):
        return (
            db.query(Property)
            .filter(
                Property.id == property_id
            )
            .first()
        )

    @staticmethod
    def get_by_external_id(db, external_id: str):
        return (
            db.query(Property)
            .filter(
                Property.external_id == external_id
            )
            .first()
        )

    # ---------------------------------------
    # Criar e salvar
    # ---------------------------------------
    @staticmethod
    def create(db, prop: Property):
        db.add(prop)
        db.flush()

        return prop

    @staticmethod
    def save(db):
        db.flush()

    # ---------------------------------------
    # Search dinâmico
    # --------------------------------------- 
    @staticmethod
    def search(
        db,

        id: int = None,
        external_id: str = None,

        city: str = None,
        state: str = None,
        source: str = None,

        title: str = None,

        min_price: float = None,
        max_price: float = None,

        min_area: float = None,
        max_area: float = None,

        active: bool = True,

        order_by: str = "created_at",
        descending: bool = False,

        limit: int = None,
        offset: int = None,

        url: str = None,

        created_after: datetime = None,
        created_before: datetime = None
    ):

        query = db.query(Property)

        # ---------------------------------------
        # Filtros
        # ---------------------------------------

        if id is not None:
            query = query.filter(
                Property.id == id
            )

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

        if url is not None:
            query = query.filter(
                Property.url.ilike(f"%{url}%")
            )

        if created_after is not None:
            query = query.filter(
                Property.created_at >= created_after
            )

        if created_before is not None:
            query = query.filter(
                Property.created_at <= created_before
            )

        # ---------------------------------------
        # Ordenação
        # ---------------------------------------

        columns = {
            "price": Property.last_price,
            "area": Property.area,
            "created_at": Property.created_at,
            "city": Property.city,
            "state": Property.state,
            "title": Property.title,
            "last_seen": Property.last_seen_at
        }

        column = columns.get(
            order_by,
            Property.created_at
        )

        if descending:
            query = query.order_by(
                desc(column)
            )
        else:
            query = query.order_by(
                asc(column)
            )

        # ---------------------------------------
        # Paginação
        # ---------------------------------------

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.all()
    

    # ---------------------------------------
    # GET ALL
    # ---------------------------------------
    @staticmethod
    def get_all(db):
        return db.query(Property).all()
    
    
    # ---------------------------------------
    # Delete para testes
    # ---------------------------------------
    @staticmethod
    def delete(db, prop: Property):
        db.delete(prop)

    # ---------------------------------------
    # Count
    # ---------------------------------------
    @staticmethod
    def count(db):
        return db.query(Property).count()