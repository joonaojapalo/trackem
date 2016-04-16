from flask import Blueprint

from flask import request
from flask_restful import Api
from flask_restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required, current_user

from db import db
from models import User, Group, Map
import login_manager
from logger import logger

# define flask blueprint 
maps_api = Blueprint('maps_api', __name__,
                        template_folder='templates')

# user get fields
map_fields = {
    "id":     	fields.Integer,
    "created":  fields.Float,
    "name":     fields.String,
    "group":    fields.Integer,
    "loc_1_lat": fields.Float,
    "loc_1_lon": fields.Float,
    "loc_1_x":  fields.Float,
    "loc_1_y":  fields.Float,
    "loc_2_lat": fields.Float,
    "loc_2_lon": fields.Float,
    "loc_2_x":  fields.Float,
    "loc_2_y":  fields.Float,
    "loc_3_lat": fields.Float,
    "loc_3_lon": fields.Float,
    "loc_3_x":  fields.Float,
    "loc_3_y":  fields.Float
}

# user writable fields
map_parser = reqparse.RequestParser()
map_parser.add_argument("name", required=True)
#map_parser.add_argument("group", type=int)
map_parser.add_argument("loc_1_lon")
map_parser.add_argument("loc_1_lat")
map_parser.add_argument("loc_1_x")
map_parser.add_argument("loc_1_y")


def read_group(current_user, group_id):
    # get group by id
    return Group.query.filter(Group.id == group_id)\
        .filter(Group.users.any(User.id == current_user.id))\
        .one()


class APIMap (Resource):
    status_deleted = "deleted"

    def read_map(self, current_user, group_id, map_id):
        # get group by id
        group = read_group(current_user, group_id)

        # query map by map_id and current_user.id
        return Map.query.\
            filter(Map.id == map_id, Map.group == group.id, Map.status != self.status_deleted).\
            one()

    @login_required
    @marshal_with(map_fields)
    def get(self, group_id, map_id):
        return self.read_map(current_user, group_id, map_id)

    @login_required
    @marshal_with({"success": fields.Boolean})
    def delete(self, group_id, map_id):
        mapobj = self.read_map(current_user, group_id, map_id)
        mapobj.status = self.status_deleted
        db.session.commit()
        return True

    @login_required
    @marshal_with(map_fields)
    def put(self, group_id, map_id):
        args = map_parser.parse_args()

        # read map
        mapobj = self.read_map(current_user, group_id, map_id)

        # set data
        attrs = ("name", "loc_1_lat", "loc_1_lon", "loc_1_x", "loc_1_y",\
                 "loc_2_lat", "loc_2_lon", "loc_2_x", "loc_2_y",\
                 "loc_3_lat", "loc_3_lon", "loc_3_x", "loc_3_y")

        for attr in attrs:
            if attr in args:
                mapobj.__setattr__(attr, args[attr])

        # TODO: if all loc_* attrs filled -> publish event
        db.session.commit()

        return mapobj


class APIMaps (Resource):
    status_deleted = "deleted"

    @login_required
    @marshal_with(map_fields)
    def get(self, group_id):

        # read authorized group
        group = read_group(current_user, group_id)

        # read undeleted maps
        return group.maps.filter(Map.status != self.status_deleted).all()

    @login_required
    @marshal_with(map_fields)
    def post(self, group_id):
        args = map_parser.parse_args()

        # get group by id
        group = read_group(current_user, group_id)

        logger.debug("User '%s' (%i) adding map: '%s' to group '%s'" % (current_user.name, current_user.id, args["name"], group.name))

        # create new map
        mapobj = Map(args["name"])

        # make group relation
        group.maps.append(mapobj)

        # commit transaction
        db.session.add(mapobj)
        db.session.commit()
        return mapobj


# init flask-restful api
api = Api(maps_api)

# user api end-points
api.add_resource(APIMaps, "/api/groups/<int:group_id>/maps")
api.add_resource(APIMap, "/api/groups/<int:group_id>/maps/<int:map_id>")
