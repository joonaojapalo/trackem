import os
import json
import unittest

from base_test_case import TrackEmTestCase

from app import app
from db import db
from models import User

# routes
from routes import *

class TestCase(TrackEmTestCase):

    def get_all_users(self):
        rv = self.app.get("/api/users")
        return json.loads(rv.data)

    def get_users_groups(self):
        rv = self.app.get("/api/groups")
        self.assertEqual(rv.status_code, 200)
        return json.loads(rv.data)

    def test_users(self):
        # create user
        user_john_obj = User('john', 'john@example.com', "secret")

        # verify password hashing
        self.assertEqual(user_john_obj.email, "john@example.com")
        self.assertFalse(user_john_obj.password_match("guessed"))
        self.assertTrue(user_john_obj.password_match("secret"))

        with app.app_context():
            db.session.add(user_john_obj)
            db.session.commit()

        # create new user by api
        users = self.get_all_users()
        self.assertEqual(len(users), 1)

        user_post = {
            "name": "Hank",
            "email": "hank@mail.com",
            "password":"hank_secret",
            "groupName": "Trackers OK"
            }

        rv = self.app.post("/api/users", data=json.dumps(user_post), headers=[('Content-Type', 'application/json')])
        user_hank_obj = json.loads(rv.data)
        self.assertEqual(user_hank_obj["name"], "Hank")
        self.assertTrue("id" in user_hank_obj)
        self.assertFalse("password" in user_hank_obj)

        # verify account created (TODO: remove public user databasequery apis)
        users = self.get_all_users()
        self.assertEqual(len(users), 2)

        # test login failure
        rv = self.app.post("/login", data={"username": "Hank", "password": "invalid_password"})
        self.assertEqual(rv.status_code, 302)
        self.assertTrue(rv.location.endswith("?fail"))

        # Hank logs in
        rv = self.app.post("/login", data={"username": "Hank", "password": "hank_secret"})
        self.assertEqual(rv.status_code, 302)
        self.assertTrue(rv.location.endswith("?success"))

        # get user groups
        groups = self.get_users_groups()
        self.assertEqual(len(groups), 1)

        # add new group
        rv = self.api_post("/api/groups", {"name": "Team 2nd"})

        groups = self.get_users_groups()
        self.assertEqual(len(groups), 2)
        expected_groups = ("Trackers OK", "Team 2nd")
        self.assertTrue(groups[0]["name"] in expected_groups)
        self.assertTrue(groups[1]["name"] in expected_groups)

        # get group from api
        rv = self.app.get("/api/groups/%i" % groups[0]["id"])
        group0 = json.loads(rv.data)
        self.assertTrue(group0["name"] == groups[0]["name"])


if __name__ == '__main__':
    unittest.main()
