requirejs.config 
	baseUrl: "static/lib"
	paths:
		app: "../app"
		templates: "../templates"
		jquery: "jquery.min"
		underscore: "underscore-min"
		backbone: "backbone-min"
		marionette: "backbone.marionette.min"
		radio: "backbone.radio.min"
		handlebars: "handlebars.amd.min"
		text: "text.min"

requirejs ["app/main"]
