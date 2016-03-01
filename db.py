import json

from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound#, MultipleResultsFound

#define db
db = SQLAlchemy(app)

__all__ = ["db"]


# format database error to api
@app.errorhandler(NoResultFound)
def handle_not_found(error):
    response = {
    	"status_code": 404,
    	"message": "not found"
    }
    return json.dumps(response), 404
