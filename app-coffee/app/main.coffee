define ["handlebars", "app/models/user", "app/views/app-layout"], (Handlebars, User, AppLayoutView) ->
	$ = require "jquery"
	Backbone = require "backbone"
	Marionette = require "marionette"

	# setup handlebars renderer
	Marionette.Renderer.render = (template, data) ->
		Handlebars.compile(template) data

	# app router
	AppRouter = Backbone.Router.extend
		routes:
			"": "dashboard"
			"maps": "maps"
			"trainings": "trainings"
			"groups": "trainings"
			"user": "user"
		dashboard: ->
#			Radio.channel("navigation")
			console.log "dashboard"			
		user: ->
			console.log "user account route"
		maps: ->
			a=1
		trainings: ->
			a=1
		groups: ->
			a=1


	appRouter = new AppRouter()

	# say when started
	appRouter.on "route", (route) ->
		console.log "maps route.", route

	# app wide models
	user = new User

	($.when user.fetch()).then ->
		appLayout = new AppLayoutView

		appLayout.on "render", ->
			Backbone.history.start()

		appLayout.render()


