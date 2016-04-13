import json
import time
import unittest

from base_test_case import TrackEmTestCase
import models

# routes
from routes import *


class TestMaps (TrackEmTestCase):
    def create_user(self, name, password, groupName):

        # create user
        user_post = {
            "name": name,
            "email": "%s@mail.com" % name.lower(),
            "password": password,
            "groupName": groupName
            }

        rv = self.app.post("/api/users", data=json.dumps(user_post), headers=[('Content-Type', 'application/json')])
        self.assertEqual(rv.status_code, 200)
        user = json.loads(rv.data)
        group = user["groups"][0]
        return user, group

    def create_map(self, group_id, map_name):
        rv = self.api_post("/api/groups/%i/maps" % group_id, {"name": map_name})
        self.assertEqual(rv.status_code, 200)

        map_obj = json.loads(rv.data)
        self.assertEqual(map_obj["name"], map_name)
        self.assertEqual(map_obj["group"], group_id)

        return map_obj

    def test_maps(self):

        # create & login user Hank
        user_hank, group_hank = self.create_user("Hank", "hank_secret", "Trackers OK")
        self.log_in_user("Hank", "hank_secret")

        # create maps
        map_a = self.create_map(group_hank["id"], "Map A")

        # update map markers
        map_a["loc_1_lat"] = 99.0;
        map_a["loc_1_lon"] = 99.1;
        map_a["loc_1_x"] = 1.0;
        map_a["loc_1_y"] = 2.0;
        rv = self.api_put("/api/groups/%i/maps/%i" % (group_hank["id"], map_a["id"]), map_a)
        updated = json.loads(rv.data)
        self.assertEqual(updated["loc_1_lat"], 99.0)
        self.assertEqual(updated["loc_1_lon"], 99.1)
        self.assertEqual(updated["loc_1_x"], 1.0)
        self.assertEqual(updated["loc_1_y"], 2.0)

        # create another map
        map_b = self.create_map(group_hank["id"], "Map B")

        # get all Hank's  maps
        rv = self.app.get("/api/groups/%i/maps" % group_hank["id"])
        group_hank_maps = json.loads(rv.data)
        print len(group_hank_maps)
        self.assertEqual(len(group_hank_maps), 2)

        # logout Hank
        self.log_out_user()

        # create and login user john
        user_john, group_john = self.create_user("John", "john_password", "OC One")
        self.log_in_user("John", "john_password")

        # create map
        rv = self.api_post("/api/groups/%i/maps" % group_john["id"], {"name": "Map C"})
        map_c = json.loads(rv.data)
        self.assertEqual(map_c["name"], "Map C")
        self.assertEqual(map_c["group"], group_john["id"])

        # get all group maps
        rv = self.app.get("/api/groups/%i/maps" % group_john["id"])
        group_john_maps = json.loads(rv.data)
        self.assertEqual(len(group_john_maps), 1)

        # test update another users map fail
        rv = self.app.get("/api/groups/%i/maps" % group_hank["id"])
        self.assertNotEqual(rv.status_code, 200)


    def test_trainings(self):

        # create and login user john
        user_john, group_john = self.create_user("John", "john_password", "OC One")
        self.log_in_user("John", "john_password")

        # create map
        map_a = self.create_map(group_john["id"], "Map A")

        # create a race
        race = {"name": "Training One", "group": group_john["id"], "map": map_a["id"]}
        rv = self.api_post("/api/groups/%i/races" % group_john["id"], race)
        self.assertEqual(rv.status_code, 200)
        race = json.loads(rv.data)
        self.assertEqual(race["name"], "Training One")
        self.assertEqual(race["status"], "stopped")

        # update race state
        race["status"] = "started"
        rv = self.api_put("/api/groups/%i/races/%i" % (group_john["id"], race["id"]), race)
        race = json.loads(rv.data)
        self.assertEqual(race["status"], "started")

        # runner requests join
        rv = self.api_post("/api/races/%s/runners/" % (race["code"]), {"runner_name": "Randy Runner"})
        randy_runner = json.loads(rv.data)
        self.assertEqual(randy_runner["status"], "new")
        self.assertEqual(randy_runner["runner_name"], "Randy Runner")
        self.assertTrue("runner_hash" in randy_runner)

        # LATER: Runner changes name
#        "/api/races/<race_code>/runners/<trace_hash>"

        # get runner requests
        rv = self.app.get("/api/groups/%i/races/%i/runners" % (group_john["id"], race["id"]))
        race_runners = json.loads(rv.data)
        self.assertEqual(len(race_runners), 1)
        self.assertEqual(race_runners[0]["runner_name"], "Randy Runner")

        # accept runner
        runner = race_runners[0]
        runner["status"] = "accept"
        rv = self.api_put("/api/groups/%i/races/%i/runners/%i" % (group_john["id"], race["id"], runner["id"]), runner)
        runner = json.loads(rv.data)
        self.assertEqual(runner["status"], "accept")

        # test get from races/runners
        rv = self.app.get("/api/groups/%i/races/%i/runners" % (group_john["id"], race["id"]))
        race_runners = json.loads(rv.data)
        self.assertEqual(len(race_runners), 1)
        self.assertEqual(race_runners[0]["runner_name"], "Randy Runner")
        self.assertEqual(race_runners[0]["status"], "accept")

        # runner submits locations
        rv = self.api_post("/api/traces/%s" % (randy_runner["runner_hash"]), {"lat": 101.0, "lon": 90.1, "time": time.time()})
        self.assertEqual(rv.status_code, 200)
        rv = self.api_post("/api/traces/%s" % (randy_runner["runner_hash"]), {"lat": 102.0, "lon": 90.2, "time": time.time()})
        rv = self.api_post("/api/traces/%s" % (randy_runner["runner_hash"]), {"lat": 103.0, "lon": 90.3, "time": time.time()})

        # TODO: get traces
        print " followinfg", race["race_hash"]
        rv = self.app.get("/api/follow/races/%s" % race["race_hash"])
        race_traces = json.loads(rv.data)
        print race_traces
        self.assertEqual(race_traces["name"], "Training One")
        self.assertEqual(len(race_traces["traces"]), 1)
        self.assertEqual(len(race_traces["traces"][0]["trace"]), 3)


if __name__ == '__main__':
    unittest.main()
