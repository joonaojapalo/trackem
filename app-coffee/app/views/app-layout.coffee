define ["radio", "marionette", "text!templates/app-layout", "app/state"], (Radio, Marionette, AppLayoutTemplate, state) ->

	AppLayout = Marionette.LayoutView.extend
		el: "body"

		template: AppLayoutTemplate

		regions:
			contentRegion: "#content"

		ui:
			username: 	'[data-ui="username"]'
			group: 		'[data-ui="group"]'

		onRender: ->
			console.log "app-layout:render"
			userChannel = Radio.channel "user"
			groupChannel = Radio.channel "group"
			userChannel.on "sync", @onUserSync
			groupChannel.on "sync", @onGroupSync
			@onUserSync()
			@onGroupSync()

		onUserSync: ->
			@ui.username.text state.get("user").get "name"

		onGroupSync: ->
			console.log "group:sync", (state.get "group").attributes
			@ui.group.text state.get("group").get("name")

