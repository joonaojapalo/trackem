from flask import request
from flask_restful import Resource, Api, fields, marshal_with, reqparse

from app import app
from db import db
import models



# rendered routes
@app.route("/", methods=["GET"])
def index():
    return "trackEm Smokes..."


# init flask-restful
api = Api(app)

# user get fields
user_fields = {
    "id":     	fields.Integer,
    "name":     fields.String,
    "email":    fields.String,
    "status":   fields.String
}

# user writable fields
user_parser = reqparse.RequestParser()
user_parser.add_argument("name")
user_parser.add_argument("email")


class User (Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        return db.session.query(models.User).filter_by(id=user_id).one()

    def delete(self, user_id):
        user = db.session.query(models.User).filter_by(id=user_id).one()
        user.status = "deleted"
        db.session.commit()
        return "true"


class Users (Resource):
    @marshal_with(user_fields)
    def get(self):
        return db.session.query(models.User).all()

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = models.User(args["name"], args["email"])
        db.session.add(user)
        db.session.commit()
        return user


# user api end-points
api.add_resource(Users, "/api/u")
api.add_resource(User, "/api/u/<int:user_id>")
