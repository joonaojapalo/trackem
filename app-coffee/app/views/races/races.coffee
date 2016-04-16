define ["radio", "app/state", "marionette", "text!templates/races/races"], (Radio, state, Marionette, template) ->

	RacesView = Marionette.ItemView.extend

		template: template

