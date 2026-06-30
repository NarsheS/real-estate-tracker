from api import Property


class PropertyRepository:

    @staticmethod
    def get_by_external_id(db, external_id: str):

        return (
            db.query(Property)
            .filter(
                Property.external_id == external_id
            )
            .first()
        )

    @staticmethod
    def create(db, property: Property):

        db.add(property)
        db.flush()

        return property

    @staticmethod
    def get_all(db):

        return db.query(Property).all()

    @staticmethod
    def save(db):

        db.flush()