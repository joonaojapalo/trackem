define ["handlebars", "radio", "app/state", "views/app-layout", "app/locales/locale", "widgets/loader"], (Handlebars, Radio, state, AppLayoutView, locale, LoaderView) ->
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

	#debug
	Radio.tuneIn "map"

	RequireRouter = Backbone.Router.extend
		requireAndShow: (layoutName, options) ->
			# start loader animation after a period, if not loaded yet
			isReady = false
			setTimeout (-> appLayout.contentRegion.show (new LoaderView) if !isReady), 200

			require ["app/views/#{layoutName}/layout"], (LayoutView) ->
				layout = new LayoutView (options ? options : {}) 

				layout.on "show", ->
					navChannel.trigger layoutName

				isReady = true
				appLayout.contentRegion.show layout


	# app router
	AppRouter = RequireRouter.extend
		routes:
			"": "dashboard"
			"maps": "maps"
			"maps/:id": "map"
			"groups": "groups"
			"user": "user"

		dashboard: ->
			@requireAndShow "dashboard"

		user: ->
			@requireAndShow "user"

		maps: ->
			@requireAndShow "maps"

		map: (id) ->
			@requireAndShow "maps",
				mapId: id

		groups: ->
			@requireAndShow "groups"


	RacesRouter = RequireRouter.extend
		routes:
			"races/race/:id": "race"
			"races": "races"

		races: ->
			@requireAndShow "races"

		race: (id)->
			(Radio.channel "races").trigger "select", parseInt(id)


	appRouter = new AppRouter()
	racesRouter = new RacesRouter()

	# start app
	($.when (state.get "user").fetch()).then ->

		appLayout.on "render", ->
			Backbone.history.start()

		appLayout.render()
