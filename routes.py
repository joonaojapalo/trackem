import json

from sqlalchemy.orm.exc import NoResultFound
from flask import request, render_template, redirect, url_for
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


# import api blueprints
from users_api import users_api
from groups_api import groups_api
from maps_api import maps_api

# register blueprints
app.register_blueprint(users_api)
app.register_blueprint(groups_api)
app.register_blueprint(maps_api)


# rendered routes
@app.route("/", methods=["GET"])
def index():
	if current_user.is_authenticated:
		return redirect(url_for("trackem_app"))
	else:
		return render_template("landing.jade")


@login_required
@app.route("/app", methods=["GET"])
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
		return redirect(url_for('trackem_app'))

	else:
		return redirect(url_for('index'))


@login_required
@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('index'))

