import os
import json
import unittest

# set test config
os.environ["APP_CONFIG"] = "config.Testing"

from flask.ext.login import login_user, logout_user

import login_manager
from app import app
from db import db

from models import User


class TrackEmTestCase(unittest.TestCase):
    def setUp(self):
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

    def api_put(self, url, data):
        """ api put request helper
        """
        return self.app.put(url, data=json.dumps(data), headers=[('Content-Type', 'application/json')])

    def log_in_user(self, username, password):
        """ login use by username in
        """
        rv = self.app.post("/login", data={"username": username, "password": password})
        self.assertEqual(rv.status_code, 302)
        self.assertTrue(rv.location.endswith("?success"))

    def log_out_user(self):
        rv = self.app.get("/logout")
        self.assertTrue(rv.location.endswith("?logout"))

    def get_basedir(self):
        return ""
