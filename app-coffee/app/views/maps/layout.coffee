define ["jquery", "radio", "underscore", "marionette", "text!templates/maps/layout", "app/state", "views/maps/dropdown", "views/maps/edit", "views/maps/empty", "widgets/loader", "stores/maps"], ($, Radio, _, Marionette, MapsLayoutTemplate, state, Dropdown, EditMapView, EmptyMapView, LoaderView, mapsStore) ->

	mapsChannel = Radio.channel("maps")

	MapsLayout = Marionette.LayoutView.extend

		template: MapsLayoutTemplate

		regions:
			mapsRegion: 	'[data-region="maps"]'
			editMapRegion: 	'[data-region="edit-map"]'

		ui:
			create: '[data-action="create"]',
			inputNewMapName: '[name="new-map-name"]'

		events:
			"click @ui.create": "onCreateClick"

		initialize: (options) ->
			_.bindAll @, "onSelect"

			@state = new Backbone.Model
				mapId: parseInt options.mapId ? null

			# when map is deleted...
			_this = @
			mapsChannel.on "delete", ->
				_this.editMapRegion.show new EmptyMapView

		onDestroy: ->
			mapsChannel.off "delete"
			mapsChannel.off "map:select"

		onBeforeShow: ->
			mapsChannel.on "map:select", @onSelect

			# fetch data
			_this = @
			mapsStore.fetch().done (maps) ->
				_this.triggerMethod "fetch", maps

		onFetch: (maps) ->
			@mapsRegion.show new Dropdown
				collection: maps

			# show map
			map = maps.findWhere
				id: @state.get "mapId"

			if not map
				@editMapRegion.show new EmptyMapView
			else
				@onSelect map

		onSelect: (map) ->
			Backbone.history.navigate "maps/#{map.get 'id'}"
			@editMapRegion.show new EditMapView
				model: map

		onCreateClick: ->
			newMapName = @ui.inputNewMapName.val()
			if !newMapName
				return

			# create map
			mapsStore.fetch().done (maps) ->
				# save
				mapAttrs =
					name: newMapName

				promise = maps.create mapAttrs,
					wait: true
					success: (model) ->
						mapsChannel.trigger "map:create", model

