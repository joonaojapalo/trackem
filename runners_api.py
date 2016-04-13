from flask import Blueprint

from flask import request
from flask_restful import Api
from flask_restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import login_required, current_user

from db import db
from models import Race, Trace, TraceLocation
from logger import logger

# define flask blueprint 
runners_api = Blueprint('runners_api', __name__,
                        template_folder='templates')

# user get fields
runner_fields = {
    "id":     	    fields.Integer,
    "name":         fields.String,
    "email":        fields.String
}

trace_fields = {
    "id":           fields.Integer,
    "runner_name":  fields.String,
    "status":       fields.String,
    "runner_hash":  fields.String
}

trace_location_fields = {
    "lat":  fields.Float,
    "lon":  fields.Float,
    "time":  fields.Float
}


# runner fields
runner_parser = reqparse.RequestParser()
runner_parser.add_argument("runner_name", required=True)

# 
trace_location_parser = reqparse.RequestParser()
trace_location_parser.add_argument("time", type=float, required=True)
trace_location_parser.add_argument("lat", type=float, required=True)
trace_location_parser.add_argument("lon", type=float, required=True)


class APIRunnerTraces (Resource):

    @marshal_with(trace_fields)
    def post(self, race_code):
        args = runner_parser.parse_args()

        # find race
        race = Race.query.filter(Race.code == race_code).one()

        # create runner
        runner_trace = Trace(args["runner_name"], race.id)

        race.traces.append(runner_trace)
        db.session.add(runner_trace)
        db.session.commit()

        logger.debug("runner created: %s" % runner_trace.runner_name)

        return runner_trace
 

class APIRunnerTrace (Resource):

    @marshal_with(trace_fields)
    def post(self, race_code, runner_hash):
        pass


class APITraceLocations (Resource):

    @marshal_with(runner_fields)
    def post(self, runner_hash):

        args = trace_location_parser.parse_args()

        # read trace
        trace = Trace.query.filter(Trace.runner_hash == runner_hash).one()

        logger.debug("new loc to trace: %i" % trace.race)

        # add location to trace
        trace_location = TraceLocation(args["time"], args["lat"], args["lon"])
        trace.locations.append(trace_location)
        db.session.add(trace_location)

        return trace_location


# init flask-restful api
api = Api(runners_api)

# runner trace api
api.add_resource(APIRunnerTraces, "/api/races/<race_code>/runners/")
api.add_resource(APIRunnerTrace, "/api/races/<race_code>/runners/<runner_hash>")
api.add_resource(APITraceLocations, "/api/traces/<runner_hash>")

