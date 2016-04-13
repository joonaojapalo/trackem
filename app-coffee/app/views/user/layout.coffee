define ["radio", "marionette", "text!templates/user-layout.html", "app/state"], (Radio, Marionette, UserLayoutTemplate, state) ->

	UserLayout = Marionette.LayoutView.extend

		template: UserLayoutTemplate

		onBeforeShow: ->
			console.log "show child views"

		onRender: ->
			console.log "init jquery widgets"
