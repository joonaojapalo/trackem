define ["radio", "app/state", "marionette", "text!templates/races/race-item", "stores/races"], (Radio, state, Marionette, template, racesStore) ->

	RaceItemView = Marionette.ItemView.extend
		tagName: "li"
		className: "list-group-item"
		template: template


	RacesView = Marionette.CollectionView.extend
		childView: RaceItemView
		tagName: "ul"
		className: "list-group"

