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
    "name":     fields.String
}

# user writable fields
map_parser = reqparse.RequestParser()
map_parser.add_argument("name", required=True)
map_parser.add_argument("group", required=True)


class APIMap (Resource):
    @login_required
    @marshal_with(map_fields)
    def get(self, group_id):
        pass


class APIMaps (Resource):
    @login_required
    @marshal_with(map_fields)
    def get(self):
        return current_user.groups

    @login_required
    @marshal_with(map_fields)
    def post(self):
        args = group_parser.parse_args()

        logger.info("adding map: %s to group %s" % (args["name"], args["group"]))

        # TODO: get group by id
        group = Group.query.filter(Group.id == args["group"]).filter(Group.users.any(User.id == current_user.id))

        map = models.Map(args["name"])
        group.maps.append(map)
        db.session.add(map)
        db.session.commit()
        return map



# init flask-restful api
api = Api(maps_api)

# user api end-points
api.add_resource(APIMaps, "/api/maps")
api.add_resource(APIMap, "/api/maps/<int:map_id>")
