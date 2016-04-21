define ["radio", "marionette", "text!templates/races/layout", "views/races/races", "views/races/runners", "views/races/player", "app/state", "views/races/create-race-layout"], (Radio, Marionette, template, RacesView, RunnersView, RacePlayerView, state, CreateRaceLayout) ->

	RacesLayout = Marionette.LayoutView.extend

		template: template

		regions:
			racesRegion: 		'[data-region="races"]'
			racePlayerRegion: 	'[data-region="race-player"]'
			runnersRegion: 		'[data-region="race-runners"]'
			createRaceRegion: 	'[data-region="create-race"]'

		childEvents:
			"select:map:change": "onSelectMap"

		initialize: (options) ->
			@mergeOptions options, ["races", "runners"]

		onBeforeShow: ->
			@racesRegion.show new RacesView
				races: @races

			@runnersRegion.show new RunnersView
				runners: @runners

			@racePlayerRegion.show new RacePlayerView
				model: @race

			@createRaceRegion.show new CreateRaceLayout

