from api import UserAlert


class AlertRepository:

    @staticmethod
    def create(db, alert: UserAlert):

        db.add(alert)
        db.flush()

        return alert


    @staticmethod
    def get_by_id(db, alert_id: int):

        return (
            db.query(UserAlert)
            .filter(
                UserAlert.id == alert_id
            )
            .first()
        )


    @staticmethod
    def get_all(db):

        return db.query(UserAlert).all()


    @staticmethod
    def get_active(db):

        return (
            db.query(UserAlert)
            .filter(
                UserAlert.active == True
            )
            .all()
        )


    @staticmethod
    def save(db):

        db.flush()


    @staticmethod
    def delete(db, alert: UserAlert):

        db.delete(alert)