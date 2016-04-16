define ["radio", "modelbinder", "marionette", "text!templates/maps/edit"], (Radio, ModelBinder, Marionette, template) ->

	mapsChannel = Radio.channel "maps"

	EditMapView = Marionette.ItemView.extend
		template: template

		ui:
			"save": 	'[data-action="save"]',
			"delete": 	'[data-action="delete"]',
			"mapName": 	'input[name="name"]'

		events:
			"click @ui.save": 		"onClickSave"
			"click @ui.delete":		"onClickDelete",
			"change @ui.mapName": 	"onChangeMapName"

		onClickSave: ->
			@ui.save.prop "disabled", true

			promise = @model.save()
			saveBtn = @ui.save
			promise.always ->
				saveBtn.prop "disabled", false

		onClickDelete: ->
			@ui.delete.prop "disabled", true
			promise = @model.destroy
				wait: true

			promise.done ->
				mapsChannel.trigger "delete"

			btn = @ui.delete
			promise.always ->
				btn.prop "disabled", false

		onChangeMapName: ->
			@model.set "name", @ui.mapName.val()
			console.debug "mapname change #{@model.get 'name'}"

