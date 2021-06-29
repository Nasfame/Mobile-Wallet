from datetime import datetime

from flask_login import UserMixin
from pytz import timezone

from . import db


def time_now():
    IST = timezone('Asia/Kolkata')
    return datetime.now(IST)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    balance = db.Column(db.Float(44))


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float(44), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=time_now())

    @property
    def repr(self):
        return {"id": self.id, "date": self.date.strftime('%d/%m/%y %H:%M:%S'), "sender_id": self.sender_id,
                "receiver_id": self.receiver_id, "amount": self.amount}

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}
