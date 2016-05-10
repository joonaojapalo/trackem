define ["radio", "underscore", "marionette", "text!templates/races/layout", "views/races/races", "views/races/runners", "views/races/player", "app/state", "views/races/create-race-layout", "stores/races"], (Radio, _, Marionette, template, RacesView, RunnersView, RacePlayerView, state, CreateRaceLayout, racesStore) ->


	RacesLayout = Marionette.LayoutView.extend

		template: template

		regions:
			racesRegion: 		'[data-region="races"]'
			racePlayerRegion: 	'[data-region="race-player"]'
			runnersRegion: 		'[data-region="race-runners"]'
			createRaceRegion: 	'[data-region="create-race"]'

		initialize: (options) ->
			_.bindAll @, "onDataFetch", "onSelectRace"
			@mergeOptions options, ["runners"]

		destroy: ->
			(Radio.channel "races").off "select"

		onBeforeShow: ->
			racesStore.fetch().done @onDataFetch

			@runnersRegion.show new RunnersView
				runners: @runners

			@createRaceRegion.show new CreateRaceLayout

		onDataFetch: (races) ->
			@races = races
			@racesRegion.show new RacesView
				collection: races

			(Radio.channel "races").on "select", @onSelectRace

			defaultRace = races.at 0
			@onSelectRace defaultRace.get "id"

		onSelectRace: (raceId) ->
			@racePlayerRegion.show new RacePlayerView
				model: @races.findWhere
					id: raceId
