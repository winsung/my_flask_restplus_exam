import datetime

from model import db

class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    last_logout_dt = db.Column(db.DateTime)
    signout_dt = db.Column(db.DateTime)
    create_dt = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<User %r>' % self.user_id

    def to_dictionary(self):
        """ for response """
        return {
            "id": self.id,
            "last_logout_dt": None if not self.last_logout_dt else str(self.last_logout_dt),
            "signout_dt": None if not self.signout_dt else str(self.signout_dt),
            "create_dt": None if not self.create_dt else str(self.create_dt)
        }