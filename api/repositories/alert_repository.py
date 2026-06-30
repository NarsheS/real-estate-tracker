from api import UserAlert


class AlertRepository:

    @staticmethod
    def get_active(db):

        return (
            db.query(UserAlert)
            .filter(
                UserAlert.active == True
            )
            .all()
        )