define ["radio", "marionette", "text!templates/races/runner-card"], (Radio, Marionette, template) ->

	RunnerCardView = Marionette.ItemView.extend
		template: template

