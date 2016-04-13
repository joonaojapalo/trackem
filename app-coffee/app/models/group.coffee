define ["backbone"], (Backbone) ->

	Group = Backbone.Model.extend

		defaults:
			name: "My club"

		urlRoot: "/api/groups/"
