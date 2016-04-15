import os

from flask import Flask
import config

__all__ = ["app"]

class JadeFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

# define APP_CONFIG
app = Flask(__name__)

# setup Flask configuration
config_obj_name = os.environ.get("APP_CONFIG", "config.Development")
app.config.from_object(config_obj_name)
