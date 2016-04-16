define ["marionette", "text!templates/maps/empty"], (Marionette, template) ->

	EmpryMapView = Marionette.ItemView.extend
		template: template
