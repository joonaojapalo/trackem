define ["radio", "marionette", "text!templates/races-layout.html", "app/state"], (Radio, Marionette, RacesLayoutTemplate, state) ->

	RacesLayout = Marionette.LayoutView.extend

		template: RacesLayoutTemplate

		regions:
			racesRegion: '[data-region="races"]'

		onBeforeShow: ->
			console.log "show child views"

		onRender: ->
			console.log "init jquery widgets"
