from flask import Blueprint, render_template, abort, current_app
from jinja2 import TemplateNotFound

client_template_dir = 'templates/clientside'

# define flask blueprint
client_side_templates = Blueprint('client_side_templates', __name__,
                        template_folder=client_template_dir)

# client-side jade templates
@client_side_templates.route("/app/templates/<path:template>", methods=["GET"])
def get_template(template):
	try:
		return render_template("%s.jade" % template)
	except TemplateNotFound:
		abort(404)
