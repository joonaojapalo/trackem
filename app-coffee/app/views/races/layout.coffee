define ["radio", "underscore", "marionette", "text!templates/races/layout", "views/races/races", "views/races/runners", "views/races/player", "app/state", "views/races/create-race-layout"], (Radio, _, Marionette, template, RacesView, RunnersView, RacePlayerView, state, CreateRaceLayout) ->


	RacesLayout = Marionette.LayoutView.extend

		template: template

		regions:
			racesRegion: 		'[data-region="races"]'
			racePlayerRegion: 	'[data-region="race-player"]'
			runnersRegion: 		'[data-region="race-runners"]'
			createRaceRegion: 	'[data-region="create-race"]'

		initialize: (options) ->
			_.bindAll @, "selectRace"
			@mergeOptions options, ["races", "runners", "raceId"]
			(Radio.channel "races").on "select", @selectRace

		onBeforeShow: ->
			@runnersRegion.show new RunnersView
				runners: @runners

			@createRaceRegion.show new CreateRaceLayout

			@racesRegion.show new RacesView
				collection: @races

			race = @getRace()
			if race
				@selectRace race

		getRace: ->
			if not @raceId
				return @races.at 0
			else
				return @races.findWhere {id: @raceId}

		selectRace: (race) ->
			@racePlayerRegion.show new RacePlayerView
				model: race
