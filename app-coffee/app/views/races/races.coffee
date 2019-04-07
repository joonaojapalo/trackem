define ["radio", "app/state", "marionette", "text!templates/races/race-item"], (Radio, state, Marionette, template) ->

	RaceItemView = Marionette.ItemView.extend
		tagName: "li"
		className: "list-group-item"
		template: template
		events:
			"click a": "selectRace"
		selectRace: (e) ->
			(Radio.channel "races").trigger "select", @model
			e.preventDefault()



	RacesView = Marionette.CollectionView.extend
		childView: RaceItemView
		tagName: "ul"
		className: "list-group"

