define ["jquery", "radio", "underscore", "marionette", "text!templates/maps-layout.html", "app/state", "app/views/maps/dropdown", "app/collections/maps", "app/views/maps/edit"], ($, Radio, _, Marionette, MapsLayoutTemplate, state, Dropdown, Maps, EditMapView) ->

	MapsLayout = Marionette.LayoutView.extend

		template: MapsLayoutTemplate

		regions:
			mapsRegion: '[data-region="maps"]'
			editMapRegion: '[data-region="edit-map"]'

		ui:
			create: '[data-action="create"]'

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

		onBeforeShow: ->

			# fetch data
			_this = @
			@maps.fetch().done ->
				_this.triggerMethod "fetch", _this.maps

			EditMapView

		onFetch: (maps) ->
			@mapsRegion.show new Dropdown
				collection: maps

		onSelect: (map) ->
			console.log "map selected: #{map.get "id"}"
			@editMapRegion.show new EditMapView
				model: map

		onCreateClick: ->
			# create map
			map = new @maps.model
				name: "My Map"
				,
					group: state.get "group"

			# save
			_t = @
			map.save().done ->
				console.log "new map save success"
				_t.maps.add map
				(Radio.channel "maps").trigger "map:create", map
