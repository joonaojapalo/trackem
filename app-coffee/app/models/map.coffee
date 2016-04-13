define ["underscore", "backbone"], (_, Backbone) ->

	Maps = Backbone.Model.extend

		urlRoot: ->
			"/api/groups/#{@get 'group'}/maps"

		initialize: (attributes) ->
			_.bindAll @, "urlRoot"
