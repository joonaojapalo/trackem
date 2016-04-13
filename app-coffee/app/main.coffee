define ["handlebars", "radio", "app/state", "app/views/app-layout", "app/locales/locale"], (Handlebars, Radio, state, AppLayoutView, locale) ->
	$ = require "jquery"
	Backbone = require "backbone"
	Marionette = require "marionette"

	# setup handlebars renderer
	Marionette.Renderer.render = (template, data) ->
		Handlebars.compile(template) data

	# setup handlebars l10n
	Handlebars.registerHelper "_", (keyword, options) ->
		return new Handlebars.SafeString(locale[state.get "locale"][keyword] ? keyword)

	# define navigation channel
	navChannel = Radio.channel "navigation"
	userChannel = Radio.channel "user"

	# app layout (attached to <body>)
	appLayout = new AppLayoutView

	# app router
	AppRouter = Backbone.Router.extend
		routes:
			"": "dashboard"
			"maps": "maps"
			"races": "races"
			"groups": "groups"
			"user": "user"

		requireAndShow: (layoutName) ->
			require ["app/views/#{layoutName}/layout"], (LayoutView) ->
				console.log "got #{layoutName} layout. rendering.."
				layout = new LayoutView

				layout.on "show", ->
					navChannel.trigger layoutName

				appLayout.contentRegion.show layout


		dashboard: ->
			@requireAndShow "dashboard"

		user: ->
			@requireAndShow "user"

		maps: ->
			@requireAndShow "maps"

		races: ->
			@requireAndShow "races"

		groups: ->
			@requireAndShow "groups"


	appRouter = new AppRouter()

	navChannel.on "maps", console.log.bind console, "navChannel:maps"

	# start app
	($.when (state.get "user").fetch()).then ->

		appLayout.on "render", ->
			Backbone.history.start()

		appLayout.render()
