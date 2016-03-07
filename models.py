import json
import time

from werkzeug.security import check_password_hash, generate_password_hash
from db import db

__all__ = ["User"]


user_groups = db.Table('user_group',
    db.Column('user', db.Integer, db.ForeignKey('user.id'), nullable=False, index=True),
    db.Column('group', db.Integer, db.ForeignKey('group.id'), nullable=False, index=True),
    db.Column('issued', db.Float, default=time.time)
)

class User(db.Model):
    __tablename__ = 'user'

    id          = db.Column(db.Integer, primary_key=True)
    created     = db.Column(db.Float, default=time.time)
    email       = db.Column(db.String(255), index=True)
    name        = db.Column(db.String(64))
    password    = db.Column(db.String(64))
    status      = db.Column(db.Enum("new", "confirmed", "deleted", name="status_enum"), nullable=False)

    # relationships
    groups = db.relationship('Group', secondary=user_groups,
                             backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name, email, password=''):
        self.created    = time.time()
        self.name       = name
        self.email      = email
        self.status     = "new"
        self.set_password(password)

    def password_match(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_authenticated(self):
        """ implements Flask-authapi
        """
        return True
 
    def is_active(self):
        """ implements Flask-authapi
        """
        return True
 
    def is_anonymous(self):
        """ implements Flask-authapi
        """
        return False
 
    def get_id(self):
        """ implements Flask-authapi
        """
        return unicode(self.id)

    def __str__(self):
        return json.dumps({"id": self.id, "email": self.email, "status": self.status, "created": self.created})

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Receipt(db.Model):
    __tablename__ = 'receipt'

    id      = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.Float, default=time.time)
    date    = db.Column(db.Integer, nullable=False)
    amount  = db.Column(db.DECIMAL, nullable=False)
    vat     = db.Column(db.DECIMAL, nullable=False)
    item    = db.Column(db.String, nullable=False)

    user    = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class UserConfirmation(db.Model):
    __tablename__ = 'user_confirmation'

    id      = db.Column(db.Integer, primary_key=True)
    hash    = db.Column(db.String, nullable=False)
    expires = db.Column(db.Integer, nullable=False)
    target  = db.Column(db.Enum("email", "password", "account", name="user_confirmation_target_enum"), nullable=False)

    user    = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)


class Group(db.Model):
    __tablename__ = 'group'
    id      = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.Float, default=time.time)
    name    = db.Column(db.String, nullable=False)

    # relations
    maps = db.relationship('Map')

    def __init__(self, name):
        self.name = name


class Payment(db.Model):
    __tablename__ = 'payment'
    id      = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.Float, default=time.time)
    user    = db.Column(db.Integer, db.ForeignKey("receipt.id"), nullable=False)
    receipt = db.Column(db.Integer, db.ForeignKey("receipt.id"), nullable=True)
    licence = db.Column(db.Integer, db.ForeignKey("receipt.id"))

#   payment_gateway_attrs
#    status  = db.Column(db.Enum("created", "success", "error", name="payment_status_enum"), nullable=False)

class License(db.Model):
    __tablename__ = 'license'
    id      = db.Column(db.Integer, primary_key=True)
    issued  = db.Column(db.Integer, nullable=False, index=True)
    expires = db.Column(db.Integer, nullable=False, index=True)
    receipt = db.Column(db.Integer, db.ForeignKey("receipt.id"), nullable=False)

class Map(db.Model):
    __tablename__ = 'map'
    id          = db.Column(db.Integer, primary_key=True)
    created     = db.Column(db.Float, default=time.time, index=True)
    name        = db.Column(db.String, nullable=False, index=True)
    is_tiles    = db.Column(db.Boolean, default=False)
    status      = db.Column(db.Enum("new", "ready", "deleted", name="map_status_enum"), nullable=False)
    loc_1_lat   = db.Column(db.Float, nullable=True)
    loc_1_lon   = db.Column(db.Float, nullable=True)
    loc_1_x     = db.Column(db.Float, nullable=True)
    loc_1_y     = db.Column(db.Float, nullable=True)
    loc_2_lat   = db.Column(db.Float, nullable=True)
    loc_2_lon   = db.Column(db.Float, nullable=True)
    loc_2_x     = db.Column(db.Float, nullable=True)
    loc_2_y     = db.Column(db.Float, nullable=True)
    loc_3_lat   = db.Column(db.Float, nullable=True)
    loc_3_lon   = db.Column(db.Float, nullable=True)
    loc_3_x     = db.Column(db.Float, nullable=True)
    loc_3_y     = db.Column(db.Float, nullable=True)
    group       = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)

    def __init__(self, name):
        self.name = name


class MapTile(db.Model):
    __tablename__ = 'map_tile'
    id      = db.Column(db.Integer, primary_key=True)
    x       = db.Column(db.Integer, index=True)
    y       = db.Column(db.Integer, index=True)
    z       = db.Column(db.Integer, index=True)
    image   = db.Column(db.LargeBinary)



class Race(db.Model):
    __tablename__ = 'race'
    id      = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.Float, default=time.time, index=True)
    name    = db.Column(db.String, nullable=False, index=True)
    code    = db.Column(db.String, index=True)
    status  = db.Column(db.Enum("stopped", "started", "deleted", name="race_status_enum"), nullable=False, default="stopped")
    start_time = db.Column(db.Integer)


class Race_control(db.Model):
    __tablename__ = 'race_control'
    id      = db.Column(db.Integer, primary_key=True)
    lat     = db.Column(db.Float, nullable=True)
    lon     = db.Column(db.Float, nullable=True)
    order   = db.Column(db.Integer)
    label   = db.Column(db.String)
    type    = db.Column(db.Enum("start", "control", "finish", name="race_control_enum"), nullable=False, default="control")


class Trace(db.Model):
    __tablename__ = 'trace'
    id          = db.Column(db.Integer, primary_key=True)           # for user access
    runner_hash = db.Column(db.String, unique=True, index=True)     # for runner access
    status      = db.Column(db.Enum("new", "accept", "reject", name="trace_status_enum"), nullable=False, default="new")
    race        = db.Column(db.Integer, db.ForeignKey("race.id"))


class Runner(db.Model):
    __tablename__ = 'runner'
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String, nullable=False)
    email   = db.Column(db.String, nullable=False)


class TraceLocation(db.Model):
    __tablename__ = 'trace_location'
    id      = db.Column(db.Integer, primary_key=True)
    trace   = db.Column(db.Integer, db.ForeignKey("trace.id"), nullable=False)
    lat     = db.Column(db.Float)
    lon     = db.Column(db.Float)
    time    = db.Column(db.Float)
