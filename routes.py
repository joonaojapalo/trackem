import json

from sqlalchemy.orm.exc import NoResultFound
from flask import request, render_template, redirect, url_for, Flask
from flask.ext.login import login_required, login_user, logout_user, current_user

from app import app
from db import db
import models
import login_manager


# format database error to api
@app.errorhandler(NoResultFound)
def handle_not_found(error):
    response = {
    	"status_code": 404,
    	"message": "not found"
    }
    return json.dumps(response), 404


# add extensions
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

# client app template
from client_side_templates import client_side_templates

# import api blueprints
from users_api import users_api
from groups_api import groups_api
from maps_api import maps_api
from races_api import races_api
from runners_api import runners_api
from follower_api import follower_api

# register blueprints
app.register_blueprint(users_api)
app.register_blueprint(groups_api)
app.register_blueprint(maps_api)
app.register_blueprint(races_api)
app.register_blueprint(runners_api)
app.register_blueprint(follower_api)
app.register_blueprint(client_side_templates)


# rendered routes
@app.route("/", methods=["GET"])
def index():
	if current_user.is_authenticated:
		return redirect(url_for("trackem_app"))
	else:
		return render_template("landing.jade")


@app.route("/app", methods=["GET"])
@login_required
def trackem_app():
	return render_template("app.jade", username=current_user.name)


@app.route("/login", methods=["POST"])
def login():
	# authenticate user
	username = request.form['username']
	password = request.form['password']

	# get user
	user = db.session.query(models.User).filter_by(name=username).one()

	if user.password_match(password):
		# grant access
		login_user(user)
		return redirect("%s?success" % url_for('trackem_app'))

	else:
		return redirect("%s?fail" % url_for('index'))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("%s?logout" % url_for('index'))


