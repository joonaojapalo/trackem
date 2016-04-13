from flask import Blueprint

from flask import request
from flask_restful import Api
from flask_restful import Resource, fields, marshal_with, reqparse

from db import db
from models import Race, Trace, TraceLocation
from logger import logger

# define flask blueprint 
follower_api = Blueprint('follower_api', __name__,
                        template_folder='templates')


trace_location_fields = {
    "lat":  fields.Float,
    "lon":  fields.Float,
    "time": fields.Float
}

trace_fields = {
    "runner_name":  fields.String,
    "trace":        fields.List(fields.Nested(trace_location_fields))
}

race_fields = {
    "name":     fields.String,
    "traces":   fields.List(fields.Nested(trace_fields))
}


class APIRaces (Resource):

    @marshal_with(race_fields)
    def get(self, race_hash):
        logger.debug(" Follow api: race_hash=%s" % race_hash)

        # read race
        race = Race.query.filter(Race.race_hash == race_hash).one()

        # read traces
        traces = race.traces.filter(Trace.status == "accept").all()

        # read and set locations
        for trace in traces:
            locs = trace.locations.all()
            logger.debug("follow trace %s locs: %s" % (race_hash, locs))
            trace.trace = locs

        # set race object
        race.traces = traces

        # return complex type
        return race


# init flask-restful api
api = Api(follower_api)

# runner trace api
# TODO: plan& clafiry timestamping / data slicing
api.add_resource(APIRaces, "/api/follow/races/<race_hash>")

