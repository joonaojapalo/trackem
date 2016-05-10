define ["jquery", "underscore", "radio", "marionette", "text!templates/races/add-modal", "widgets/select", "stores/maps", "stores/races", "app/models/race", "app/state"], ($, _, Radio, Marionette, template, SelectView, mapsStore, racesStore, Race, state) ->

	CreateRaceLayout = Marionette.LayoutView.extend
		template: template

		regions:
			mapsRegion: 		'[data-region="maps-dropdown"]'

		ui:
			name: 		'[name="race-name"]'
			createBtn:  '[data-action="create"]'

		events:
			'click @ui.createBtn':  "onCreate"
			"keyup @ui.name": 		"onNameChange"

		mountData: [mapsStore, racesStore]

		initialize: ->
			_.bindAll @, "mount", "onCreate", "onSelectMapChange", "onNameChange"

			@race = new Race
				group: state.get "group"

			@race.on "error", @onInvalid

			# fetch data
			@promises = _.invoke @mountData, "fetch"

		onBeforeShow: ->
			all = $.when.apply @, @promises
			all.done @mount

		mount: (maps, races) ->
			@races = races

			select = new SelectView
				prefix: "select:map"
				collection: maps
				nameAttr: "name"
				valueAttr: "id"

			select.on "select:map:change", @onSelectMapChange

			@mapsRegion.show select

		onSelectMapChange: (model) ->
			@race.set "map", model.get "id"

		onNameChange: ->
			@race.set "name", @ui.name.val()

		onInvalid: (error) ->
			console.log "invalid", error

		onCreate: ->

			if @race.validate
				return

			@races.create @race,
				wait: true

