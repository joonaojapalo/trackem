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

class APIMap (Resource):

    @login_required
    @marshal_with(map_fields)
    def get(self, group_id, map_id):
        pass

    @login_required
    @marshal_with(map_fields)
    def put(self, group_id, map_id):
        args = map_parser.parse_args()

        # get group by id
        group = Group.query\
            .filter(Group.id == group_id)\
            .filter(Group.users.any(User.id == current_user.id))\
            .one()

        # query map by map_id and current_user.id
        mapobj = Map.query.\
            filter(Map.id == map_id, Map.group == group.id).\
            one()

        # set data
        attrs = ("name", "loc_1_lat", "loc_1_lon", "loc_1_x", "loc_1_y",\
                 "loc_2_lat", "loc_2_lon", "loc_2_x", "loc_2_y",\
                 "loc_3_lat", "loc_3_lon", "loc_3_x", "loc_3_y")

        for attr in attrs:
            if attr in args:
                mapobj.__setattr__(attr, args[attr])

        # TODO: if all loc_* attrs filled -> compute projection
        db.session.commit()

        return mapobj


class APIMaps (Resource):

    @login_required
    @marshal_with(map_fields)
    def get(self, group_id):

        # get group by id
        group = Group.query.filter(Group.id == group_id)\
            .filter(Group.users.any(User.id == current_user.id))\
            .one()

        return group.maps.all()

    @login_required
    @marshal_with(map_fields)
    def post(self, group_id):
        args = map_parser.parse_args()

        # get group by id
        group = Group.query.filter(Group.id == group_id)\
            .filter(Group.users.any(User.id == current_user.id))\
            .one()

        logger.debug("User '%s' (%i) adding map: '%s' to group '%s'" % (current_user.name, current_user.id, args["name"], group.name))

        mapobj = Map(args["name"])
        group.maps.append(mapobj)
        db.session.add(mapobj)
        db.session.commit()
        return mapobj


# init flask-restful api
api = Api(maps_api)

# user api end-points
api.add_resource(APIMaps, "/api/groups/<int:group_id>/maps")
api.add_resource(APIMap, "/api/groups/<int:group_id>/maps/<int:map_id>")
