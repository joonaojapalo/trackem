define ["underscore", "backbone"], (_, Backbone) ->

	Race = Backbone.Model.extend
		defaults:
			name:  ""
			map:   ""
			group: ""

		validate:
			if !(@get "name"):
				return "name"
			if !(@get "group"):
				return "group"

			map = @get "map"
			if map == "" or not parseInt map:
				return "map"

