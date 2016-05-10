from flask import Blueprint

from flask import request
from flask_restful import Api
from flask_restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required, current_user

from db import db
from models import User, Group, Map, Race, Trace
import login_manager
from logger import logger

# define flask blueprint 
races_api = Blueprint('races_api', __name__,
                        template_folder='templates')

# output fields
race_fields = {
    "id":     	fields.Integer,
    "created":  fields.Float,
    "name":     fields.String,
    "map":      fields.Integer,
    "group":    fields.Integer,
    "status":   fields.String,
    "code":     fields.String,
    "race_hash": fields.String
}

# input arguments
race_parser = reqparse.RequestParser()
race_parser.add_argument("name", required=True)
race_parser.add_argument("map", required=True, type=int)
race_parser.add_argument("status", choices=("stopped", "started"))


class APIRace (Resource):

    @login_required
    @marshal_with(race_fields)
    def get(self, group_id, race_id):
        pass

    @login_required
    @marshal_with(race_fields)
    def put(self, group_id, race_id):
        args = race_parser.parse_args()

        # get group by id
        group = Group.query\
            .filter(Group.id == group_id)\
            .filter(Group.users.any(User.id == current_user.id))\
            .one()

        # query race by race_id and current_user.id
        race = Race.query.\
            filter(Race.id == race_id, Race.group == group.id).\
            one()

        logger.debug(" race found: %s, %s"% (race.name, race.code))

        for attr in ("name", "status"):
            if attr in args:
                race.__setattr__(attr, args[attr])

        db.session.commit()
        return race


class APIRaces (Resource):

    @login_required
    @marshal_with(race_fields)
    def get(self, group_id):

        # get group by id
        group = Group.query.filter(Group.id == group_id)\
            .filter(Group.users.any(User.id == current_user.id))\
            .one()

        return group.races.all()

    @login_required
    @marshal_with(race_fields)
    def post(self, group_id):
        args = race_parser.parse_args()

        # get group by id
        group = Group.query.filter(Group.id == group_id)\
            .filter(Group.users.any(User.id == current_user.id))\
            .one()

        logger.debug("User '%s' (%i) creates race: '%s' to group '%s'" % (current_user.name, current_user.id, args["name"], group.name))

        race = Race(args["name"], args["map"])
        group.races.append(race)
        db.session.add(race)
        db.session.commit()
        return race



# output fields
trace_fields = {
    "id":           fields.Integer,
    "runner_name":  fields.String,
    "status":       fields.String,
    "runner_hash":  fields.String
}

# input arguments
trace_parser = reqparse.RequestParser()
trace_parser.add_argument("status", choices=("accept", "reject"), required=True)


class APIRaceRunners (Resource):

    @login_required
    @marshal_with(trace_fields)
    def get(self, group_id, race_id):

        # get group by id
        group = Group.query\
            .filter(Group.id == group_id)\
            .filter(Group.users.any(User.id == current_user.id))\
            .one()

        # get race
        race = Race.query.\
            filter(Race.id == race_id, Race.group == group.id).\
            one()

        # return runner traces
        return race.traces.all()


class APIRaceRunner (Resource):

    @login_required
    @marshal_with(trace_fields)
    def get(self, group_id, race_id, runner_id):
        pass

    @login_required
    @marshal_with(trace_fields)
    def put(self, group_id, race_id, runner_id):

        args = trace_parser.parse_args()

        # get group by id
        group = Group.query\
            .filter(Group.id == group_id)\
            .filter(Group.users.any(User.id == current_user.id))\
            .one()

        # get race
        race = Race.query.\
            filter(Race.id == race_id, Race.group == group.id).\
            one()

        # get runner trace
        trace = Trace.query.\
            filter(Trace.id == runner_id, Trace.race == race.id).\
            one()

        # update 
        trace.status = args["status"]
        db.session.commit()

        return trace


# init flask-restful api
api = Api(races_api)

# user api end-points
api.add_resource(APIRaces, "/api/groups/<int:group_id>/races")
api.add_resource(APIRace, "/api/groups/<int:group_id>/races/<int:race_id>")
api.add_resource(APIRaceRunners, "/api/groups/<int:group_id>/races/<int:race_id>/runners")
api.add_resource(APIRaceRunner, "/api/groups/<int:group_id>/races/<int:race_id>/runners/<int:runner_id>")
