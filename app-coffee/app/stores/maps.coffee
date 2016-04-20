define ["app/state", "app/store", "app/collections/maps"], (state, Store, Maps) ->

	MapsStore = Store.extend

		fetchableClass: Maps

		setup: ->
			@fetchable.group = state.get "group"
			@listenTo state, "change:group", @refetch
			console.log "fetchable:", @fetchable

	new MapsStore
