define ["jquery", "radio", "underscore", "marionette", "text!templates/maps/layout", "app/state", "app/views/maps/dropdown", "app/collections/maps", "app/views/maps/edit", "app/views/maps/empty"], ($, Radio, _, Marionette, MapsLayoutTemplate, state, Dropdown, Maps, EditMapView, EmptyMapView) ->

	MapsLayout = Marionette.LayoutView.extend

		template: MapsLayoutTemplate

		regions:
			mapsRegion: '[data-region="maps"]'
			editMapRegion: '[data-region="edit-map"]'

		ui:
			create: '[data-action="create"]',
			inputNewMapName: '[name="new-map-name"]'

		events:
			"click @ui.create": "onCreateClick"

		initialize: (options) ->
			_.bindAll @, "onSelect"
			@state = new Backbone.Model
				mapId: options.mapId ? null

			 mapsChannel = Radio.channel("maps")
			 mapsChannel.on "map:select", @onSelect

			# init maps collection
			@maps = new Maps [],
				group: state.get "group"

			# when map is deleted...
			_this = @
			mapsChannel.on "delete", ->
				_this.editMapRegion.show new EmptyMapView

		onBeforeShow: ->

			# fetch data
			_this = @
			@maps.fetch().done ->
				_this.triggerMethod "fetch", _this.maps

			@editMapRegion.show new EmptyMapView

		onFetch: (maps) ->
			@mapsRegion.show new Dropdown
				collection: maps

		onSelect: (map) ->
			console.log "map selected: #{map.get "id"}"
			@editMapRegion.show new EditMapView
				model: map

		onCreateClick: ->
			newMapName = @ui.inputNewMapName.val()
			if !newMapName
				return

			# create map
			map = new @maps.model
				name: newMapName
				group: (state.get "group").get "id"

			# save
			_t = @
			map.save().done ->
				console.log "new map save success"
				_t.maps.add map
				(Radio.channel "maps").trigger "map:create", map
