define ["radio", "marionette", "text!templates/dashboard-layout.html", "app/state"], (Radio, Marionette, DashboardLayoutTemplate, state) ->

	DashboardLayout = Marionette.LayoutView.extend

		template: DashboardLayoutTemplate

		regions:
			recentMapsRegion: 	'[data-region="recent-maps"]'
			recentRacesRegion: 	'[data-region="recent-races"]'
			licenseRegion: 		'[data-region="license"]'

		onBeforeShow: ->
			console.log "show child views"

		onRender: ->
			console.log "init jquery widgets"
