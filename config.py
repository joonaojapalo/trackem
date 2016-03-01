import os

class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'localhost'

class Production(Config):
    DEBUG = False
