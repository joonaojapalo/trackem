define ["underscore", "backbone"], (_, Backbone) ->

	Map = Backbone.Model.extend
		defaults:
			name: ""
