define ["marionette", "text!templates/app-layout.html"], (Marionette, AppLayoutTemplate) ->

	AppLayout = Marionette.LayoutView.extend
		el: "body"
		template: AppLayoutTemplate
		templateHelpers:
			username: "goom"
			user: 
				name: "Joona"
			group:
				name: "Lynx"
