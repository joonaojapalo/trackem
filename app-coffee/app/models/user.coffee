define ["backbone"], (Backbone) ->
	User = Backbone.Model.extend
		defaults:
			name: 	""
			email:  ""
			groups: []

		url: "/api/users/~"
