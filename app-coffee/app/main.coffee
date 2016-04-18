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

	# app router
	AppRouter = Backbone.Router.extend
		routes:
			"": "dashboard"
			"maps": "maps"
			"maps/:id": "map"
			"races": "races"
			"groups": "groups"
			"user": "user"

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


		dashboard: ->
			@requireAndShow "dashboard"

		user: ->
			@requireAndShow "user"

		maps: ->
			@requireAndShow "maps"

		map: (id) ->
			@requireAndShow "maps",
				mapId: id

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
