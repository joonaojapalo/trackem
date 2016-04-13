from flask import Blueprint

from flask import request
from flask_restful import Api
from flask_restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required, current_user

from logger import logger
from db import db
from models import User, Group
import login_manager


# define flask blueprint 
users_api = Blueprint('users_api', __name__,
                        template_folder='templates')

# user get fields
user_fields = {
    "id":     	fields.Integer,
    "name":     fields.String,
    "email":    fields.String,
    "status":   fields.String,
    "groups":   fields.List(fields.Nested({
	    "id":     	fields.Integer,
	    "created":  fields.Float,
	    "name":     fields.String
	}))
}

# user writable fields
post_user_parser = reqparse.RequestParser()
post_user_parser.add_argument("name", required=True)
post_user_parser.add_argument("password", required=True)
post_user_parser.add_argument("email")
post_user_parser.add_argument("groupName")



class APIUser (Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        return User.query.filter_by(id=user_id).one()

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).one()
        user.status = "deleted"
        db.session.commit()
        return "true"


class APIUsers (Resource):
    @marshal_with(user_fields)
    def get(self):
        return User.query.all()

    @marshal_with(user_fields)
    def post(self):
        args = post_user_parser.parse_args()

        # prepare args
        username = args["name"]
        group_name = args["groupName"] if args["groupName"] is not None else "%s's Group" % username.capitalize()

        # add user group relation
        user = User(username, args["email"], args["password"])
        group = Group(group_name)
        user.groups = [group]
        db.session.add(user)
        db.session.add(group)
        db.session.commit()

        logger.info("user read: %s" % str(user))
        return user


class APIMyUser (Resource):
    @login_required
    @marshal_with(user_fields)
    def get(self):
        return User.query.filter_by(id=current_user.id).one()

    @login_required
    @marshal_with(user_fields)
    def put(self):
        return ""


# init flask-restful api
api = Api(users_api)

# user api end-points
api.add_resource(APIUsers, "/api/users")
api.add_resource(APIUser, "/api/users/<int:user_id>")
api.add_resource(APIMyUser, "/api/users/~")
