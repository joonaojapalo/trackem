define ["radio", "marionette", "text!templates/groups-layout.html", "app/state"], (Radio, Marionette, GroupsLayoutTemplate, state) ->

	GroupsLayout = Marionette.LayoutView.extend

		template: GroupsLayoutTemplate

		regions:
			groupsRegion: '[data-region="groups"]'

		onBeforeShow: ->
			console.log "show child views"

		onRender: ->
			console.log "init jquery widgets"
