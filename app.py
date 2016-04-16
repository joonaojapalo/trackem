import os

from flask import Flask
import config

__all__ = ["app"]

# define APP_CONFIG
app = Flask(__name__)

# setup Flask configuration
config_obj_name = os.environ.get("APP_CONFIG", "config.Development")
app.config.from_object(config_obj_name)
