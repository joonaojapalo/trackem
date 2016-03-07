from app import app

from flask.ext.login import LoginManager

#import db
from models import User

import logging

__all__ = ["login_manager"]

# create login manager 
login_manager = LoginManager()
login_manager.init_app(app)

# define user loading
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

