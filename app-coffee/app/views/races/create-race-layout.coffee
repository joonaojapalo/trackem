define ["jquery", "underscore", "radio", "marionette", "text!templates/races/add-modal", "widgets/select", "stores/maps"], ($, _, Radio, Marionette, template, SelectView, mapsStore) ->

	CreateRaceLayout = Marionette.LayoutView.extend
		template: template

		regions:
			mapsRegion: 		'[data-region="maps-dropdown"]'

		initialize: ->
			_.bindAll @, "mount"
			@mapsPromise = mapsStore.fetch()

		onBeforeShow: ->
			$.when(@mapsPromise).done @mount

		mount: (maps) ->
			@mapsRegion.show new SelectView
				prefix: "select:map"
				collection: maps
				nameAttr: "name"
				valueAttr: "id"

		onSelectMap: (model) ->
			console.log "select:change", model
