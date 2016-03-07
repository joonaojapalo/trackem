import json
import unittest

from base_test_case import TrackEmTestCase
import models

# routes
from routes import *


class TestMaps (TrackEmTestCase):
    def test_maps(self):

    	# create user
        user_post = {
            "name": "Hank",
            "email": "hank@mail.com",
            "password":"hank_secret",
            "groupName": "Trackers OK"
            }

        rv = self.app.post("/api/users", data=json.dumps(user_post), headers=[('Content-Type', 'application/json')])
        user_hank = json.loads(rv.data)
        group_hank = user_hank["groups"][0]

        # login john for testing
        self.log_in_user("Hank")

        # create maps
        map_data = {
            "name": "Map A",
            "group": group_hank["id"]
        }

        rv = self.api_post("/api/maps", map_data)
        print rv.data
        self.assertEqual(rv.status_code, 200)


if __name__ == '__main__':
    unittest.main()
