import os

from flask import Flask
import config

__all__ = ["app"]

# define app
app = Flask(__name__)

# setup Flask configuration
config_obj_name = os.environ.get("APP_CONFIG", "config.Development")
app.config.from_object(config_obj_name)

# add extensions
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

