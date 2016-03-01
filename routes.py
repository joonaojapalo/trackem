from flask import request

from app import app
#from db import db
#from models import *


# rendered routes
@app.route("/", methods=["GET"])
def index():
	return "trackEm Smokes..."

