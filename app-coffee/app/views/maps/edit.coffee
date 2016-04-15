define ["radio", "modelbinder", "marionette", "text!templates/maps/edit"], (Radio, ModelBinder, Marionette, template) ->

	EditMapView = Marionette.ItemView.extend
		template: template

		ui:
			"save": 	'[data-action="save"]'
			"mapName": 	'input[name="name"]'

		events:
			"click @ui.save": 		"onClickSave"
			"change @ui.mapName": 	"onChangeMapName"

		onClickSave: ->
			@ui.save.prop "disabled", true

			promise = @model.save()
			saveBtn = @ui.save
			promise.done ->
				console.debug "map save success"
				saveBtn.prop "disabled", false

			promise.fail ->
				saveBtn.prop "disabled", false

		onChangeMapName: ->
			@model.set "name", @ui.mapName.val()
			console.debug "mapname change #{@model.get 'name'}"
