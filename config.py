import os

class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ["SECRET_KEY"]
    BUNDLE_ERRORS = True


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class Development(Config):
    DEBUG = True

class Production(Config):
    DEBUG = False
