define ["radio", "app/state", "underscore", "marionette", "text!templates/races/player"], (Radio, state, _, Marionette, template) ->

	RacePlayerView = Marionette.ItemView.extend

		className: ->
			if (@model.get "status") == "started"
				return "race-player race-player-started"
			else
				return "race-player race-player-stopped"

		template: template

		templateHelpers: ->
			followUrl: "#{state.const.url.followAPI}/#{@model.get "race_hash"}"

		ui:
			start: '[data-action="start"]'
			stop: '[data-action="stop"]'

		events:
			"click @ui.start": "start"
			"click @ui.stop": "stop"

		modelEvents:
			"change:status": "onStatusChange"

		onRender: ->
			@onStatusChange()

		start: ->
			promise = @model.save {status: "started"}, {wait: true}

		stop: ->
			promise = @model.save {status: "stopped"}, {wait: true}

		onStatusChange: ->
			status = (@model.get "status")

			@$el.removeClass()
			@$el.addClass @className()	

			if status == "started"
				@ui.start.addClass "hidden"
			else
				@ui.start.removeClass "hidden"

			if status == "stopped"
				@ui.stop.addClass "hidden"
			else
				@ui.stop.removeClass "hidden"

