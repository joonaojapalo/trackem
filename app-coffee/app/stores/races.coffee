define ["app/state", "app/store", "app/collections/races"], (state, Store, Races) ->

	MapsStore = Store.extend

		fetchableClass: Races

		setup: ->
			@fetchable.group = state.get "group"
			@listenTo state, "change:group", @refetch

	new MapsStore
