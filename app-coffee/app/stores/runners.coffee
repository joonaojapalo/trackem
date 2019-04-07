define ["app/state", "app/store", "app/collections/runners"], (state, Store, Runners) ->

	RunnersStore = Store.extend

		fetchableClass: Runners

		setup: ->
			@fetchable.group = state.get "group"
			@fetchable.raceId = @getOption "raceId"
			@listenTo state, "change:group", @refetch

	new RunnersStore
