import os
import json
import unittest

from flask.ext.login import login_user, logout_user

import login_manager
from app import app
from db import db

from models import User


class TrackEmTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        basedir = ""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(self.get_basedir(), 'test.db')
        self.app = app.test_client()

        with app.app_context():
            db.create_all()
            print " * test database created"

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def api_post(self, url, data):
        """ api post request helper
        """
        return self.app.post(url, data=json.dumps(data), headers=[('Content-Type', 'application/json')])

    def log_in_user(self, username):
        """ login use by username in
        """

        with app.test_request_context():
            user = User.query.filter_by(name=username).one()
            login_user(user)

        return user

    def get_basedir(self):
        return ""
