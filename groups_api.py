from flask import Blueprint

from flask import request
from flask_restful import Api
from flask_restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required, current_user

from db import db
from models import Group
import login_manager


# define flask blueprint 
groups_api = Blueprint('groups_api', __name__,
                        template_folder='templates')

# user get fields
group_fields = {
    "id":     	fields.Integer,
    "created":  fields.Float,
    "name":     fields.String
}

# user writable fields
group_parser = reqparse.RequestParser()
group_parser.add_argument("name", required=True)


class APIGroup (Resource):
    @login_required
    @marshal_with(group_fields)
    def get(self, group_id):
        return Group.query.filter(Group.id==group_id).filter(Group.users.any(id=2)).one()
        #db.session.query(Group).join(models.UserGroup).filter(models.UserGroup.user==current_user.id).one()

    @login_required
    @marshal_with(group_fields)
    def put(self, group_id):
        args = group_parser.parse_args()
        group = Group.query.filter(Group.id==group_id).filter(Group.users.any(id=2)).one()
        group.name = args["name"]
        db.session.commit()
        return group


class APIGroups (Resource):
    @login_required
    @marshal_with(group_fields)
    def get(self):
        return current_user.groups

    @login_required
    @marshal_with(group_fields)
    def post(self):
        args = group_parser.parse_args()
        group = Group(args["name"])
        current_user.groups.append(group)
        db.session.add(group)
        db.session.commit()
        return group


# init flask-restful api
api = Api(groups_api)

# user api end-points
api.add_resource(APIGroups, "/api/groups")
api.add_resource(APIGroup, "/api/groups/<int:group_id>")
