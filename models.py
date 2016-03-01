from db import db
import json


__all__ = ["User"]


class User(db.Model):
    __tablename__ = 'user'

    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(), index=True)
    name        = db.Column(db.String())
    password    = db.Column(db.String())
    status      = db.Column(db.Enum("new", "confirmed", "deleted", name="status_enum"), nullable=False)

    def __init__(self, name, email, password=''):
        self.name       = name
        self.email      = email
        self.password   = password
        self.status     = "new"

    def __str__(self):
        return json.dumps({"id": self.id, "email": self.email, "status": self.status})

    def __repr__(self):
        return '<id {}>'.format(self.id)

