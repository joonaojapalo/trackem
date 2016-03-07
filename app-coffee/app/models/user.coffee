define ["backbone"], (Backbone) ->
	User = Backbone.Model.extend
		url: "/api/users/~"
		say: (msg) ->
			console.log @get "name"
