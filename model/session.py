import datetime

from model import db

class Session(db.Model):
    session_id = db.Column(db.String(20), primary_key=True)
    logout_dt = db.Column(db.DateTime)
    id = db.Column(db.String(20))
    client_ip = db.Column(db.String(15))
    create_dt = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<User %r>' % self.user_id

    def to_dictionary(self):
        """ for response """
        return {
            "session_id": self.session_id,
            "logout_dt": None if not self.logout_dt else str(self.logout_dt),
            "client_ip": self.client_ip,
            "create_dt": None if not self.create_dt else str(self.create_dt)
        }
