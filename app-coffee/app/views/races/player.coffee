define ["radio", "app/state", "marionette", "text!templates/races/player"], (Radio, state, Marionette, template) ->

	RacePlayerView = Marionette.ItemView.extend
	
		template: template

		templateHelpers: ->
			race_hash = "abc" #@model ? @model.get 'race_hash' : ""
			followUrl: "#{state.const.url.followAPI}/#{race_hash}"

