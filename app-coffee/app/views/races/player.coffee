define ["radio", "app/state", "underscore", "marionette", "text!templates/races/player"], (Radio, state, _, Marionette, template) ->

	RacePlayerView = Marionette.ItemView.extend
	
		template: template

		templateHelpers: ->
			followUrl: "#{state.const.url.followAPI}/#{@model.get "race_hash"}"

		ui:
			start: '[data-action="start"]'
			stop: '[data-action="stop"]'

		events:
			"click @ui.start": "start"
			"click @ui.stop": "stop"

		initialize: ->
			#_.bindAll @, "toggle"
			@model.on "change", @render

		onRender: ->
			status = (@model.get "status")
			console.log "render", status
#			if status == "started"
#				@ui.stop.addClass "hidden"
			#when "stopped" then @ui.start.addClass "hidden"

		start: ->
			promise = @model.save {status: "started"}, {wait: true}

		stop: ->
			promise = @model.save
				status: "stopped"
